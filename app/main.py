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

models.Base.metadata.create_all(bind=engine)  # check model and if not created in db then create them, it not update them if we alter any column



app = FastAPI()




@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}




##CRUD


@app.get("/posts", response_model=List[schemas.PostResponse])  # to get list of post, we will need List from typing
def get_posts(db: Session = Depends(get_db)):


    posts=db.query(models.Post).all()
    return posts  #fastapi will automatically serialize my list to json

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse )
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
 
    print(post.model_dump())
    
    new_post = models.Post(**post.model_dump()) # unpacking list (**) ... since schema match with db 
    db.add(new_post)  #execute query
    db.commit()
    db.refresh(new_post) # returing the value with column name similar to RETURNING *  ... it will return a sqlalchemy model 


    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse ) #{id} is a path parameter
def get_post(id:int, db: Session = Depends(get_db)):  #fastapi automatically extract id , and pydantic validating it


    post= db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    del_post= db.query(models.Post).filter(models.Post.id == id)




    
    if del_post.first() == None:          # if id did not exist then 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    del_post.delete(synchronize_session=False)
    db.commit()
    

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):


    post_query = db.query(models.Post).filter(models.Post.id == id)  # for checking wether id exist nor not

    post = post_query.first()
   

    if post == None:  # if not exist then 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False) # since id exists , now updading values via this new query

    db.commit() 



    return post_query.first() # returning query data



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password
    hashed_password = utils.hash(user.password)
    user.password=hashed_password

    new_user = models.User(**user.model_dump()) 
    db.add(new_user)  
    db.commit()
    db.refresh(new_user) 

    return new_user
    
@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} does not exist")
    
    return user
