from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException


books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publish_date": "1925-04-10",
    },
    {
        "id": 2,
        "title": "The garri to small things",
        "author": "F. Scott Fitzgerald",
        "publish_date": "1925-04-10",
    },
    {
        "id": 3,
        "title": "The rice and beans history",
        "author": "F. Scott Fitzgerald",
        "publish_date": "1925-04-10",
    },
    {
        "id": 4,
        "title": "The amala love world",
        "author": "F. Scott Fitzgerald",
        "publish_date": "1925-04-10",
    },

]

app = FastAPI()

@app.get("/book")
def get_books():
    return books

@app.get("/book/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

class Book(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str

@app.post("/book")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book

class BookUpdate(BaseModel):
    title: str
    author: str
    publish_date: str

@app.put("/book/{book_id}")
def update_book(book_id: int, updated_book: BookUpdate):
   for book in books:
        if book['id'] == book_id:
            book['title'] = updated_book.title
            book['author'] = updated_book.author
            book['publish_date'] = updated_book.publish_date
            return book
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
