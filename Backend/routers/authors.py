from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import create_connection
import objects
import tables
from hashing import Hash
from oauth2 import get_current_user, allow_users
router = APIRouter(
    prefix='/authors',
    tags=["Authors"]
)


@router.get("/authors", response_model=List[objects.showAuthor])
def get_all_authors(db: Session = Depends(create_connection), current_user: objects.Author = Depends(get_current_user)):
    authors = db.query(tables.Author).order_by(tables.Author.author_id.asc())

    return authors



@router.get('/{author_id}', response_model=objects.showAuthor)
def get_author(id: int, db: Session = Depends(create_connection), current_user: objects.Author = Depends(get_current_user)):
    author_details = db.query(tables.Author).filter(tables.Author.author_id==id).first()

    if not author_details:
       raise HTTPException(status.HTTP_404_NOT_FOUND, "Author not found")

    return author_details



@router.post('/author-register', response_model=objects.showAuthor, status_code=status.HTTP_201_CREATED)
def create_author(author: objects.Author, db: Session = Depends(create_connection), current_user: objects.Author = Depends(allow_users(['admin@mail.com']))):
    new_author = tables.Author(author_id=author.author_id, username=author.username, pwd=Hash.hashPwd(author.pwd), email=author.email, books_number=author.books_number)

    existing_author = db.query(tables.Author).filter(tables.Author.author_id==author.author_id).first()
    if existing_author:
       raise HTTPException(status.HTTP_409_CONFLICT,"Author already exists")

    try:
         db.add(new_author)
         db.commit()
         db.refresh(new_author)
    except:
         db.rollback()
         raise SystemError("New articles registration has been failed")

    return(new_author)



@router.delete('/author-delete/{author_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_author(id: int, db: Session = Depends(create_connection), current_user: objects.Author = Depends(allow_users(['admin@mail.com']))):
    droppedAuthor = db.query(tables.Author).filter(tables.Author.author_id == id).first()

    if not droppedAuthor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Author does not exist')

    try:
        db.delete(droppedAuthor)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, detail="Author deletion has been failed")

    return {"done": "Author {droppedAuthor.author_id} has been deleted"}