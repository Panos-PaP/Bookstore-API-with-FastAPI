from pydantic import BaseModel
from typing import Optional, List


class Author(BaseModel):
    author_id: int
    username: str
    email: Optional[str]
    pwd: str
    books_number: int


class Article(BaseModel):
    article_id: int
    title: str
    description: str
    viewers: int
    published: Optional[bool] = 0
    author_id: int


class ArticleName(BaseModel):
    title: str

    class Config():
       from_attributes = True


class showAuthor(BaseModel):
    username: str
    email: Optional[str]
    books_number: int
    articles: List[ArticleName] = []

    class Config():
         from_attributes = True


class showArticle(BaseModel):
    title: str
    description: str
    viewers: int
    author: showAuthor

    class Config():
         from_attributes = True



class Authentication(BaseModel):
    email: str
    pwd: str


class Token(BaseModel):
     access_token: str
     token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None