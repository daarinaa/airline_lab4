from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy import text

DATABASE_URL = "postgresql://student:mis2025!@176.108.247.125:5432/mis2025"

engine = create_engine(DATABASE_URL, echo=True)

def create_schema_and_tables():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS nigamatulina"))
        conn.commit()
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session