from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import create_connection
import objects
import tables
from oauth2 import get_current_user, allow_users

router = APIRouter (
    prefix='/articles',
    tags=['Books']
)


@router.get('/', response_model=List[objects.showArticle])
def get_all_articles(db: Session = Depends(create_connection), current_user: objects.Author = Depends(get_current_user)):
    articles_list = db.query(tables.Article).order_by(tables.Article.article_id.asc())

    return articles_list


@router.get('/{article_id}', status_code=status.HTTP_200_OK, response_model=objects.showArticle, tags=["Books"])
def get_article(id: int, db: Session = Depends(create_connection), current_user: objects.Author = Depends(get_current_user)):
   article_details = db.query(tables.Article).filter(tables.Article.article_id==id).first()

   if not article_details:
      raise HTTPException(status.HTTP_404_NOT_FOUND, "Article not found")

   return article_details



@router.post('/article-register', status_code=status.HTTP_201_CREATED)
def create_article(article: objects.Article, db: Session= Depends(create_connection), current_user: objects.Author = Depends(allow_users(['admin@mail.com']))):
    new_article = tables.Article(article_id=article.article_id, title=article.title, description=article.description, viewers=article.viewers, published=article.published, author_id=article.author_id)

    existing_article = db.query(tables.Article).filter(tables.Article.article_id==article.article_id).first()
    if existing_article:
       raise HTTPException(status.HTTP_409_CONFLICT, "Article already exists")

    try:
         db.add(new_article)
         db.commit()
         db.refresh(new_article)
    except:
         db.rollback()
         raise SystemError("New article registration has been failed")

    return(new_article)



@router.delete('/article-delete/{article_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int, db: Session = Depends(create_connection),  current_user: objects.Author = Depends(allow_users(['admin@mail.com']))):
    droppedArticle = db.query(tables.Article).filter(tables.Article.article_id == id).first()

    if not droppedArticle:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Article does not exist')

    try:
         db.delete(droppedArticle)
         db.commit()
    except:
         db.rollback()
         raise SystemError("Article deletion has been failed")

    return {"done": "Article {droppedArticle.article_id} has been deleted"}



@router.put('/article-update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_article(id: int, article: objects.Article, db: Session = Depends(create_connection),  current_user: objects.Author = Depends(allow_users(['admin@mail.com']))):
    article = db.query(tables.Article).filter(tables.Article.article_id == id)

    if not article.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Article does not exist')

    try:
      article.update({'title': article.title, 'description': article.description, 'viewers': article.viewers})
      db.commit()
    except:
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, detail="Article update has been failed")

    return {'updated article':article}
