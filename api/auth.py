from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .database import db, User
from .schemas import Token
from passlib.hash import pbkdf2_sha256

from .token import create_access_token

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=Token)
async def login(body:OAuth2PasswordRequestForm = Depends()):
    query = User.select().where(User.c.username == body.username)
    user = await db.fetch_one(query=query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found.")
    if not pbkdf2_sha256.verify(body.password, user.get('password')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not authorized.")
    access_token = create_access_token(
        data={"sub": body.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}
