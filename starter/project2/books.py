from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
  id: int
  title: str
  author: str
  description: str
  rating: float
  published_date: int

  def __init__(self, id, title, author, description, rating, published_date):
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating
    self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length = 1, max_length = 100)
    rating: float = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1970, lt=2025)

    class Config:
      json_schema_extra = {
        "example": {
          "title": "A new book",
          "author": "CodingWithNsikak",
          "description": "A valid description",
          "rating": 5,
          "published_date": 2013
        }
      }

class BookUpdateRequest(BookRequest):
  class Config:
      json_schema_extra = {
        "example": {
          "id": 1,
          "title": "A new book",
          "author": "CodingWithNsikak",
          "description": "A valid description",
          "rating": 2
        }
      }

BOOKS = [
  Book(1, "Computer Science Pro", "codingWithRoby", "A very nice book", 5, 2020),
  Book(2, "Be Fast with FastAPI", "codingWithRoby", "A great book", 5, 2022),
  Book(3, "Master Endpoints", "codingWithRoby", "Awesome book", 5, 1980),
  Book(4, "HP1", "Author 1", "Book description", 2, 2018),
  Book(5, "HP2", "Author 2", "Book description", 3, 2019),
  Book(6, "HP3", "Author 3", "Book description", 1, 2020)
]

def find_book_id(book: Book):
  # if len(BOOKS) > 0:
  #   book.id = BOOKS[-1].id + 1
  # else:
  #   book.id = 1
  book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

  return book

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
  return BOOKS


@app.get("/books/rating", status_code=status.HTTP_200_OK)
async def read_book_rating(rating: int = Query(gt=0, lt=6)):
  rating_list = []
  for book in BOOKS:
    if book.rating == rating:
      rating_list.append(book)
  return {f"books with {rating} star(s)": rating_list}

@app.get("/books/date", status_code=status.HTTP_200_OK)
async def read_book_by_year(published_date: str = Query(gt=1970, lt=2025)):
  books_to_return = []
  print(published_date)
  for book in BOOKS:
    if book.published_date == int(published_date):
      books_to_return.append(book)
      return books_to_return
  
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
  for book in BOOKS:
    if book.id == int(book_id):
       return {"book": book}
  raise HTTPException(status_code=404, detail="Item not found")

@app.post("/books/create", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
  new_book = Book(**book_request.dict())
  print(new_book)
  BOOKS.append(find_book_id(new_book))

@app.put("/books/update/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_req: BookUpdateRequest):
  book_swapped = False
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book_req.id:
      BOOKS[i] = Book(**book_req.dict())
      book_swapped = True
  if book_swapped:
    return {"new_book": book_req}
  else:
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int=Path(gt=0)):
  book_deleted = False
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book_id:
      BOOKS.pop(i)
      book_deleted = True
      break

  if not book_deleted:
    raise HTTPException(status_code=404, detail="Book not found")
  else:
    return {"message": "Book deleted"}
