from fastapi import FastAPI, UploadFile, staticfiles, Request
from fastapi.responses import PlainTextResponse
from sqlmodel import Session, select
from src.db import Book, engine
from src.utls import mime_to_extension
from pathlib import Path
import os
from uuid import uuid4

app = FastAPI(
    version='0.0.1',
    description='Is the backend for the books app, a book notetaker and note search engine',
)

app.mount('/static', staticfiles.StaticFiles(directory='static'), name='static')


@app.post('/book')
async def new_book(book: Book):
    with Session(engine) as localSession:
        localSession.add(book)
        localSession.commit()
    return PlainTextResponse("Created")

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
    return result

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