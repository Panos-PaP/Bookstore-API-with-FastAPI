from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

import tables, objects
from database import create_connection
from hashing import Hash
from login_token import create_access_token

router = APIRouter(
    tags=['Authentication']
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post('/login')
async def authentication(request: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(create_connection)) -> objects.Token:
    author = db.query(tables.Author).filter(tables.Author.email==request.username).first()

    # If author found, generate a JWT token
    if not author:
       raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    if not Hash.verify_password(request.password, author.pwd):
       raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

    access_token = create_access_token(
        data={"email": author.email}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return objects.Token(access_token=access_token, token_type="bearer")
