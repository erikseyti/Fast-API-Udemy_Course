from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
  id: UUID
  title: str = Field(min_length=1)
  author: str = Field(min_length=1, max_length=100)
  description: Optional[str] = Field(title='Description of the Book',
                           min_length=1,
                           max_length=100)
  rating: int = Field(gt=-1, lt=101)

  class Config:
    schema_extra = {
      'example': {
        'id': '95e8ed25-5ef7-4148-a227-454ec39e65c0',
        'title': 'Computer Science is Awesome',
        'author': 'Erik',
        'description': 'this is a book',
        'rating': 20
      }
    }


BOOKS = []



@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
  if len(BOOKS) < 1:
    create_books_no_api()

  if books_to_return and len(BOOKS) >= books_to_return >0:
    i = 1
    new_books = []
    while i <= books_to_return:
      new_books.append(BOOKS[i-1])
      i +=1

    return new_books

  return BOOKS


@app.post('/')
async def create_book(book: Book):
  BOOKS.append(book)
  return book


def create_books_no_api():
  book_1 = Book(id='95e8ed25-5ef7-4148-a227-454ec39e65c0', title='Title1', author='author', description='desc', rating=11)


  book_2 = Book(id='95e8ed25-5ef7-4148-a227-454ec39e65c0', title='Title1', author='author', description='desc', rating=11)

  book_3 = Book(id='95e8ed25-5ef7-4148-a227-454ec39e65c0', title='Title2', author='authorx', description='descx', rating=12)

  book_4 = Book(id='95e8ed25-5ef7-4148-a227-454ec39e65c0', title='Title3', author='authory', description='descy', rating=15)

  BOOKS.append(book_1)
  BOOKS.append(book_2)
  BOOKS.append(book_3)
  BOOKS.append(book_4)