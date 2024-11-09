from fastapi import FastAPI, UploadFile, staticfiles, Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from src.db import Book, engine, Note
from src.utls import mime_to_extension
from pathlib import Path
import os
from uuid import uuid4

app = FastAPI(
    version='0.0.1',
    description='Is the backend for the books app, a book notetaker and note search engine',
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', staticfiles.StaticFiles(directory='static'), name='static')


@app.post('/book')
async def new_book(book: Book):

    with Session(engine) as localSession:
        localSession.add(book)
        localSession.commit()
        statement = select(Book)
        last = localSession.exec(statement).all()
    return last[-1]

@app.put('/book/{book_id}', response_model=Book | None)
async def book_image(book_id: int, image: UploadFile, request: Request):
    result = None
    if image.content_type in ['image/jpeg', 'image/png', 'image/webp']:
        
       with Session(engine) as session:
           statement = select(Book).where(Book.id == book_id)
           result = session.exec(statement).first()
           ns_uuid = str(uuid4())
           ext = await mime_to_extension(image.content_type)
           with Path(f'./static/{ns_uuid}{ext}').open('wb') as f:
               f.write(image.file.read())
           result.cover = os.path.join(f'/static/{ns_uuid}{ext}')
           session.add(result)
           session.commit()
    return PlainTextResponse('Correct')

@app.get('/books')
async def books():
    with Session(engine) as session:
        statement = select(Book)
        result = session.exec(statement).all()
    return result

@app.get('/books/{id}')
async def book(id: int):
    with Session(engine) as session:
        statement = select(Book).where(Book.id == id)
        result = session.exec(statement).first()
    return result

@app.post('/note/{book_id}')
async def new_note(note: Note, book_id: int):
    with Session(engine) as localSession:
        book = localSession.exec(select(Book).where(Book.id == book_id)).first()
        localSession.add(note)
        note.book = book
        localSession.commit()
        statement = select(Note)
        last = localSession.exec(statement).all()
    return last[-1]

@app.get('/notes/{book_id}')
async def list_notes(book_id: int):
    with Session(engine) as session:
        statement = select(Book).where(Book.id == book_id)
        result = session.exec(statement).first().notes

    return result

@app.get('/note/{note_id}')
async def get_note(note_id: int):
    with Session(engine) as session:
        statement = select(Note).where(Note.id == note_id)
        result = session.exec(statement).first()
    return result

@app.put('/note/{note_id}')
async def edit_note(note: Note, note_id: int):
    with Session(engine) as session:
        statement = select(Note).where(Note.id == note_id)
        result:Note = session.exec(statement).first()
        result.book_pages = note.book_pages
        result.color = note.color 
        result.content = note.content
        result.title = note.title
        result.topic = note.topic
        result.tags = note.tags
        session.add(result)
        session.commit()
    return result