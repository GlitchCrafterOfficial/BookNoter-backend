from sqlmodel import Field, SQLModel, create_engine, Relationship
from pathlib import Path
import datetime

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cover: str | None # Link to the cover static files direction
    short_title: str | None
    title: str | None
    author: str | None
    description: str | None
    page_count: int | None
    keywords: str | None
    isbn: str | None
    doi: str | None
    notes: list["Note"] = Relationship(back_populates="book")

class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str | None
    content: str | None # Markdown content
    book_pages: str | None # Pages of the book for the note 
    color: str | None # Note color
    date_added: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now())
    tags: str | None
    topic: str | None
    book_id: int | None = Field(default=None, foreign_key='book.id')
    book: Book | None = Relationship(back_populates="notes")

sqlite_file_name = "books.db"  


sqlite_url = f"sqlite:///{sqlite_file_name}"  

engine = create_engine(sqlite_url, echo=True)  


def create_db_and_tables():
    if not Path(sqlite_file_name).exists():
        SQLModel.metadata.create_all(engine) 

create_db_and_tables()