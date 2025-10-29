# schema/pydantic model for req/res valdidation
from pydantic import BaseModel
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


    class Config:    # convets sqlachemy model to dict
        orm_model = True