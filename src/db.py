from sqlmodel import Field, SQLModel, create_engine
from pathlib import Path

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cover: str | None # Link to the cover static files direction
    title: str | None
    author: str | None
    description: str | None
    page_count: int | None
    keywords: str | None
    isbn: str | None
    doi: str | None
    
sqlite_file_name = "books.db"  


sqlite_url = f"sqlite:///{sqlite_file_name}"  

engine = create_engine(sqlite_url, echo=True)  


def create_db_and_tables():
    if not Path(sqlite_file_name).exists():
        SQLModel.metadata.create_all(engine) 

create_db_and_tables()