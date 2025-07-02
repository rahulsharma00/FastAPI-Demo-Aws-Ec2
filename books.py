from fastapi import FastAPI, Body  #type:ignore
from pydantic import BaseModel  #type:ignore

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    category: str

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

####################################################################--GET--################################################################################

'''
@app.get("/api-endpoint")  # decorative
def first_api():   # api endpoint
    return {"message": "Hello Rahul!"}
'''
'''   
@app.get("/api-endpoint")  # decorative
def first_api():   # api endpoint
    return BOOKS
'''

@app.get("/books")  # decorative
def read_all_books():   # api endpoint
    return BOOKS

'''
@app.get("/books/mybook")  # static route
async def read_all_books():
    return {"book title ": "my favourite book!"}
'''

@app.get("/books/param/{dynamic_parameter}")
def dynamic_para(dynamic_parameter: str):
    return {'dynamic_parameter': dynamic_parameter}


@app.get("/books/title/{book_title}")
def get_book_title(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}

@app.get("/books/{category}")
async def read_category(category :str):
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            return book 
    return {"message": "category not found"}

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/book/{book_author}/")
async def get_book_author(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


###############################################################--POST--####################################################################################

@app.post("/book/create_book")
async def create_book(new_book: Book):
    BOOKS.append(new_book.dict())  # This is important!
    return {"message": "Book added successfully", "book": new_book}

@app.post("/books/create_book_another_way")
async def create_book_method_two(newbook = Body()):
    BOOKS.append(newbook)

###############################################################--PUT--####################################################################################

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}
    return {"message": "Book not found"}

###############################################################--DELETE--####################################################################################

@app.delete("/books/delete_book")
def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {"message": f"'{book_title}' deleted successfully"}
    return {"message": "Book not found"}