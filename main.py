from fastapi import FastAPI,Body,Path,Query,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from starlette import status
app=FastAPI()
class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    def __init__(self,id,title,author,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
class BookRequest(BaseModel):
    id:Optional[int]=Field(description="id is not needed on create",default=None)
    title:str=Field(min_length=3)
    author:str=Field(min_length=3)
    description:str=Field(max_length=50)
    rating:int=Field(gt=0,lt=6)
    model_config={
        "json_schema_extra":{
            "examples":[
                {
                    "title":"book",
                    "author":"author",
                    "description":"description1",
                    "rating":5
                }
            ]
        }
    }
BOOKS=[Book(1,"book1","author1","description1",5),Book(2,"book2","author2","description2",4),Book(3,"book3","author3","description3",3)]
@app.get("/books",status_code=status.HTTP_200_OK)
async def root():
    return BOOKS
@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book:BookRequest):
    createdbook=Book(**book.model_dump())
    BOOKS.append(find_book_id(createdbook))
    return f"{createdbook.description}appednded"
@app.delete("/delete-book",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id:int=Query(gt=0)):
    book_deleted=False
    for book in BOOKS:
        if book.id==id:
            book_deleted=True
            BOOKS.remove(book)
            return f"{book.title} deleted"
    if(not book_deleted):
        raise HTTPException(status_code=404,detail="Book not found")
def find_book_id(book):
    if(len(BOOKS)>0):
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    return book
@app.put("/books/update",status_code=status.HTTP_200_OK)
async def update_books(books:BookRequest):
    book_changed=False
    for book in BOOKS:
        if book.id==books.id:
            book_changed=True
            book.title=books.title
            book.author=books.author
            book.description=books.description
            book.rating=books.rating
            return f"{book.title} updated"
    if(not book_changed):
       raise HTTPException(status_code=404,detail="Book not found")
@app.get("/book/{id}",status_code=status.HTTP_200_OK)
async def get_book(id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==id:
            return book
    raise HTTPException(status_code=404,detail="Book not found")
@app.get("/books/",status_code=status.HTTP_200_OK)
async def get_books(rating:int=Query(gt=0,lt=6)):
    print(Body())
    return([book for book in BOOKS if book.rating==rating])
