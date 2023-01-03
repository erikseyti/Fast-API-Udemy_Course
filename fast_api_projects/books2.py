from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
  def __init__(self, books_to_return):
    self.books_to_return = books_to_return

book_description = 'Description of the Book'

app = FastAPI()

class Book(BaseModel):
  id: UUID
  title: str = Field(min_length=1)
  author: str = Field(min_length=1, max_length=100)
  description: Optional[str] = Field(title=book_description,
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

class BookNoRating(BaseModel):
  id: UUID
  title: str = Field(min_length=1)
  author: str
  description: Optional[str] = Field(None, title=book_description, min_length=1, max_length=100)

BOOKS = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):

  return JSONResponse(
    status_code=418, content={'message': f'Hey, why do you want {exception.books_to_return} books? you need to read more!!'
    }
  )

def raise_item_cannot_be_found_exception():
  return HTTPException(status_code=404, detail='Book not found', 
                    headers={'X-Header-Error': 'Nothing to be seen at the UUID'})


@app.post('/books/login')
async def book_login(username: str = Form(), password: str = Form()):
  return {'username': username, 'password': password}


@app.get('/header')
async def read_header(random_header: Optional[str] = Header()):
  return {'Random-Header': random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
  if books_to_return and books_to_return < 0:
    raise NegativeNumberException(books_to_return=books_to_return)

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

@app.get('/book/{book_id}')
async def read_book(book_id:UUID):
  for x in BOOKS:
    if x.id == book_id:
      return x
  
  raise raise_item_cannot_be_found_exception()

@app.get('/book/rating/{book_id}', response_model=BookNoRating)
async def read_book_no_rating(book_id:UUID):
  for x in BOOKS:
    if x.id == book_id:
      return x
  
  raise raise_item_cannot_be_found_exception()

@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
  BOOKS.append(book)
  return book

@app.put('/{book_id}')
async def update_book(book_id: UUID, book: Book):
  counter = 0

  for x in BOOKS:
    counter = +1
    if x.id == book_id:
      BOOKS[counter - 1] = book
      return BOOKS[counter - 1]
  
  raise raise_item_cannot_be_found_exception()


@app.delete('/{book_id}')
async def delete_book(book_id: UUID):
  counter = 0

  for x in BOOKS:
    counter +=1
    if x.id == book_id:
      del BOOKS[counter - 1]
      return f'ID: {book_id} deleted'
  
  raise raise_item_cannot_be_found_exception()



def create_books_no_api():
  book_1 = Book(id='95e8ed25-5ef7-4148-a227-454ec39e65c0', title='Title1', author='author', description='desc', rating=11)


  book_2 = Book(id='ba524c6b-4cc5-45c6-b869-915b0701d6bf', title='Title1', author='author', description='desc', rating=11)

  book_3 = Book(id='0e25ccb3-3daf-4501-942a-788af97e7c49', title='Title2', author='authorx', description='descx', rating=12)

  book_4 = Book(id='6c1ecee5-f07c-4e50-8db2-81819fd03756', title='Title3', author='authory', description='descy', rating=15)

  BOOKS.append(book_1)
  BOOKS.append(book_2)
  BOOKS.append(book_3)
  BOOKS.append(book_4)
