from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from .database import db, Article
from .schemas import ArticleSchemaIn, ArticleSchemaOut, UserSchemaOut
from .token import get_current_user

router = APIRouter(tags=["Articles"])


@router.get('/articles', response_model=List[ArticleSchemaOut],
            status_code=status.HTTP_200_OK)
async def get_articles(current_user: UserSchemaOut = Depends(get_current_user)):
    query = Article.select()
    return await db.fetch_all(query=query)


@router.get('/articles/{id}', response_model=ArticleSchemaOut)
async def get_article_details(id: int, current_user: UserSchemaOut = Depends(
    get_current_user)):
    query = Article.select().where(id == Article.c.id)
    article = await db.fetch_one(query=query)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Article not found.")
    return article


@router.post('/articles', status_code=status.HTTP_201_CREATED,
             response_model=ArticleSchemaOut)
async def create_article(body: ArticleSchemaIn,
                         current_user: UserSchemaOut = Depends(
                             get_current_user)):
    query = Article.insert().values(title=body.title,
                                    description=body.description)
    last_record_id = await db.execute(query)
    return {**body.dict(), "id": last_record_id}


@router.put('/articles/{id}', response_model=ArticleSchemaOut)
async def get_article_details(id: int, body: ArticleSchemaIn,
                              current_user: UserSchemaOut = Depends(
                                  get_current_user)):
    query = Article.update().where(id == Article.c.id).values(
        title=body.title, description=body.description)
    await db.execute(query)
    return {**body.dict(), "id": id}


@router.delete('/articles/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int, current_user: UserSchemaOut = Depends(
    get_current_user)):
    query = Article.delete().where(Article.c.id == id)
    await db.execute(query)
