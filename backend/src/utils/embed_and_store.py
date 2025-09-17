from vector_db.pg_vector_db import PGVectorDB
import json
from pathlib import Path


if __name__ == '__main__':

    semantic_search = PGVectorDB(collection_name='qa_collection')

    dir = Path(__file__).parent.parent.parent
    env_path = Path('data/qa.json')

    texts = None
    metadata = None

    with open(env_path) as f:
        data = json.load(f)

        metadata = data
        texts = [x['question'] for x in data]
        
        for m_data in metadata:
            del m_data['question']

    new_inserts = semantic_search.insert(texts=texts, metadata=metadata)
    print(f'Numer of new inserts: {new_inserts}')