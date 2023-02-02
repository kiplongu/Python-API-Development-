from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
   
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password: str

#code for making request not sending back pssword to the user

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    #converts regular pydantic model
    class Config:
        orm_mode = True
   

class UserLogin(BaseModel):
    email: EmailStr
    password: str

#schema for token 

class Token(BaseModel):
    access_token: str
    token_type: str

#schema for token data

class TokenData(BaseModel):
    id: Optional[str] = None
