from typing import List
from fastapi import APIRouter, HTTPException, status
from .database import db, User
from .schemas import UserSchemaIn, UserSchemaOut

from passlib.hash import pbkdf2_sha256

router = APIRouter(tags=["Users",])

@router.get('/users', response_model=List[UserSchemaOut],
         status_code=status.HTTP_200_OK)
async def get_users():
    query = User.select()
    return await db.fetch_all(query=query)

@router.get('/users/{id}', response_model=UserSchemaOut)
async def get_user_details(id:int):
    query = User.select().where(id == User.c.id)
    user = await db.fetch_one(query=query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found.")
    return user

@router.post('/users', status_code=status.HTTP_201_CREATED,
          response_model=UserSchemaOut)
async def create_user(body:UserSchemaIn):
    hased_password = pbkdf2_sha256.hash(body.password)
    query = User.insert().values(username=body.username,
                                    password=hased_password)
    last_record_id = await db.execute(query)
    return {**body.dict(), "id": last_record_id}

@router.put('/users/{id}', response_model=UserSchemaOut)
async def get_user_details(id:int, body:UserSchemaIn):
    query = User.update().where(id == User.c.id).values(username=body.username,
                                    password=body.password)
    await db.execute(query)
    return {**body.dict(), "id": id}

@router.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:int):
    query = User.delete().where(User.c.id==id)
    await db.execute(query)