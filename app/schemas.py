# schema/pydantic model for req/res valdidation
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):  # api ka schema ( datatype ) 
    title: str
    content: str
    published: bool = True # defalut value is True even if your doesnt provide
   
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime


    class Config:    # convets sqlachemy model to pydantic model/dict
        orm_model = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:    # convets sqlachemy model to pydantic model/dict
        orm_model = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    