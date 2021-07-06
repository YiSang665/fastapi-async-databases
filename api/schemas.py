from typing import Optional

from pydantic import BaseModel

class ArticleSchemaIn(BaseModel):
    title: str
    description: str

class ArticleSchemaOut(ArticleSchemaIn):
    id: int

class UserSchemaIn(BaseModel):
    username: str
    password: str

class UserSchemaOut(BaseModel):
    id: int
    username: str

class LoginSchema(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None