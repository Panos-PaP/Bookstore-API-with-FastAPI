from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, nullable=False, index=False)
    username = Column(String)
    email = Column(String)
    pwd = Column(String)
    books_number = Column(Integer)

    articles = relationship("Article", back_populates="author")

class Article(Base):
    __tablename__ = 'articles'

    article_id = Column(Integer, primary_key=True, nullable=False, index=False)
    title = Column(String)
    description = Column(String)
    viewers = Column(Integer)
    published = Column(Boolean)
    author_id = Column(Integer, ForeignKey('authors.author_id'))

    author = relationship("Author", back_populates="articles")
