# import os
# from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, text
# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy.types import UserDefinedType
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# DB_USER = os.getenv("POSTGRESS_USER")
# DB_PASSWORD = os.getenv("POSTGRESS_PASS")
# DB_NAME = os.getenv("POSTGRESS_NAME")
# DB_HOST = os.getenv("POSTGRESS_HOST")
# DB_PORT = os.getenv("POSTGRESS_PORT")


# engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
# Session = sessionmaker(bind=engine)
# session = Session()
# Base = declarative_base()

# class TestTable(Base):
#     __tablename__ = "test_table"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

# Base.metadata.create_all(engine)  # Creates table if not exists

# # --- 2. Insert data ---
# row1 = TestTable(name="Alice")
# row2 = TestTable(name="Bob")
# session.add_all([row1, row2])
# session.commit()

# # --- 3. Query data ---
# results = session.query(TestTable).all()
# for r in results:
#     print(r.id, r.name)

# # --- 4. Delete a row ---
# row_to_delete = session.query(TestTable).filter_by(name="Alice").first()
# if row_to_delete:
#     session.delete(row_to_delete)
#     session.commit()

# # --- 5. Drop the table ---
# TestTable.__table__.drop(engine)
# print("Table dropped.")

if __name__ == '__main__':
    from src.vector_db.pg_vector_db import PGVectorDB

    t = PGVectorDB('qa_collection')
    r = t.search('Change profile information')
    # print(r)
    print(r['metadata']['answer'])
    print(r['score'])
