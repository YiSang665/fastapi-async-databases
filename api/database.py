from sqlalchemy import Column, Integer, String, MetaData, Table, create_engine

from databases import Database

DATABASE_URL = "postgresql://developer:secret@localhost:5432/db"

engine = create_engine(DATABASE_URL)

metadata = MetaData()

Article = Table(
    "article",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(128)),
    Column("description", String(256))
)

User = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(128)),
    Column("password", String(128))
)

db = Database(DATABASE_URL)