from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "Science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "Science"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{title}")
async def get_single_book(title: str):
    for book in BOOKS:
        if book["title"].casefold() == title.casefold():
            return {"book": book}
        else:
            return {"detail": "Book not found"}


@app.get("/books/")
async def get_category(category: str):
    books_to_return = []
    for book in BOOKS:
        if book["category"].casefold() == category.casefold():
            books_to_return.append(book)

    return (books_to_return)


@app.get("/all_books/{book_author}")
async def get_books_by_author(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold():
            books_to_return.append(book)
    return (books_to_return)


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return (books_to_return)


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    print(BOOKS)
    return({"message": "New book created successfully"})

             
@app.put("/books/update")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book
    print(BOOKS)
    return {"message": "Your book has been updated"}

@app.delete("/books/delete/{book_title}")
async def delete_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            BOOKS.remove(book)
            break
    print(BOOKS)
    return {"message": "Book deleted successfully"}
