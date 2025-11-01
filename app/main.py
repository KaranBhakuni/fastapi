#CURD WITH ORM

from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body


from typing import Optional, List
from random import randrange
import psycopg
# from psycopg.extars import RealDictCursor
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session # this Session will be used in routs, to access db
from .database import engine, get_db # engine establish connection btw db and orm 
from . import models, schemas, utils
from .routers import posts, user, auth

models.Base.metadata.create_all(bind=engine)  # check model and if not created in db then create them, it not update them if we alter any column



app = FastAPI()

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}




##CRUD

