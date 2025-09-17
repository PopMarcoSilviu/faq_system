from langchain_openai import OpenAIEmbeddings
from sqlalchemy import Row, create_engine
from dotenv import load_dotenv
from typing import Any, Union, List
import os
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine, text
import hashlib
import json

class PGVectorDB:
   
    def __init__(self, collection_name: str) -> None:
        load_dotenv()
        db_user = os.getenv("POSTGRESS_USER")
        db_pass = os.getenv("POSTGRESS_PASS")
        db_name = os.getenv("POSTGRESS_NAME")
        db_host = os.getenv("POSTGRESS_HOST")
        db_port = os.getenv("POSTGRESS_PORT")
        self.embedding_size = os.getenv("EMBEDDING_SIZE")

        embedding_model = os.getenv("EMBEDDING_MODEL", "")
       
        
        connection_string = f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        
        self.engine = create_engine(connection_string,
                                    poolclass=QueuePool,
                                    pool_size=3,          
                                    max_overflow=20,       
                                    pool_pre_ping=True,
                                    pool_timeout = 30,    
                                    pool_recycle=3600)
        self.collection_name = collection_name

        setup_sql = """CREATE EXTENSION IF NOT EXISTS vector;"""

        with self.engine.begin() as conn:
            conn.execute(text(setup_sql))

        self.change_collection(self.collection_name)

    def change_collection(self, collection_name: str) -> None:
        self.collection_name = collection_name

        create_table_sql = f"""
                        CREATE TABLE IF NOT EXISTS {self.collection_name} (
                        id BIGSERIAL PRIMARY KEY,
                        content TEXT,
                        hash VARCHAR(32),
                        metadata JSONB,
                        embedding VECTOR({self.embedding_size})  
                    );"""
        
        index_sql = f"""CREATE INDEX IF NOT EXISTS {self.collection_name}_embedding_hnsw_idx
                        ON {self.collection_name}
                        USING hnsw (embedding vector_cosine_ops)
                        WITH (m = 16, ef_construction = 200);
                        """
        
        with self.engine.begin() as conn:
            conn.execute(text(create_table_sql))
            conn.execute(text(index_sql))
    
    
    def insert(self, texts: Union[str, List[str]],
               metadata: Union[dict[Any,Any], List[dict[Any,Any]]]
               ) -> int:
        
        new_inserts = 0
       
        if isinstance(texts, str):
            texts = [texts]
           
        if isinstance(metadata, dict):
            metadata = [metadata]
            
        if len(texts) != len(metadata):
            raise ValueError(f"Different lengths: {len(texts)} texts, {len(metadata)} metadata entries")
       
        new_texts = []
        new_metadata = []
        embeddings = []
        hashes = []
        
        for text_data, m_data in zip(texts, metadata):
            text_hash = hashlib.md5(text_data.encode("utf-8")).hexdigest()

            
            filter_hash_sql = f"""SELECT 1 FROM {self.collection_name} 
                                WHERE hash = :hash_value LIMIT 1"""
           
            with self.engine.begin() as conn:
                exists_in_db = conn.execute(text(filter_hash_sql), 
                                          {"hash_value": text_hash}).first()
                
            # Check if document with this hash already exists (cheating)
            if not exists_in_db:
                new_texts.append(text_data)
                hashes.append(text_hash)
                new_metadata.append(m_data)  
                embeddings.append(self.embeddings.embed_query(text_data))
                new_inserts += 1

        if new_texts:
            with self.engine.begin() as conn:
                for text_data, m_data, emb, hash in zip(new_texts, new_metadata, embeddings, hashes):
                    insert_sql = f"""INSERT INTO {self.collection_name} (content, metadata, embedding, hash)
                    VALUES (:content, :metadata, :embedding, :hash)
                    """

                    conn.execute(text(insert_sql), 
                                      {"content": text_data, "metadata":json.dumps(m_data), "embedding": emb, "hash": hash})
        
        return new_inserts
    

    def search(self, query:str, top_k:int=1) ->  List[dict[Any, Any]]:

        embedding = self.embeddings.embed_query(query)

        query_sql = f"""SELECT *, (1 -(embedding <=> CAST(:query_embedding AS vector))) AS score FROM {self.collection_name} ORDER BY embedding <=> CAST(:query_embedding AS vector) LIMIT :top_k;"""

        with self.engine.begin() as conn:
            result = conn.execute((text(query_sql)), {"query_embedding":embedding, "top_k":top_k}).fetchall()
            return [row._asdict() for row in result]
            
      