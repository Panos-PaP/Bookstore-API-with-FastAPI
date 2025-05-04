from fastapi import FastAPI, Depends, status, HTTPException
from routers import authors,books,login


app = FastAPI(
    title="Project Alpha",
    version="1.0.0",
    debug=True
)


@app.get('/', tags=["Homepage"])
def read_root():
    return {'message': 'Welcome to the Bookstore'}


app.include_router(login.router)
app.include_router(books.router)
app.include_router(authors.router)
