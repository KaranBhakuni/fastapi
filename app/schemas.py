# schema/pydantic model for req/res valdidation
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated

# from pydantic.types import conint


class PostBase(BaseModel):  # api ka schema ( datatype ) 
    title: str
    content: str
    published: bool = True # defalut value is True even if your doesnt provide
   
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:    # convets sqlachemy model to pydantic model/dict
        orm_model = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut    # tell who created post


    class Config:    # convets sqlachemy model to pydantic model/dict
        orm_model = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

# class TokenData(BaseModel):
#     id: Optional[str]= None

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    # dir: conint(ge=0, le=1)  # ge = greater or equal, le = less or equal, coint will be deprecated in v3 pydantic
    dir: Annotated[int, Field(ge=0, le=1)]