from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session # this Session will be used in routs, to access db
from .. import models, schemas, utils
from ..database import engine, get_db # engine establish connection btw db and orm 

router=APIRouter( prefix="/posts",
                 tags=['Posts'])    # all the api will come under Posts section



@router.get("/", response_model=List[schemas.PostResponse])  # to get list of post, we will need List from typing
def get_posts(db: Session = Depends(get_db)):


    posts=db.query(models.Post).all()
    return posts  #fastapi will automatically serialize my list to json

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse )
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
 
    print(post.model_dump())
    
    new_post = models.Post(**post.model_dump()) # unpacking list (**) ... since schema match with db 
    db.add(new_post)  #execute query
    db.commit()
    db.refresh(new_post) # returing the value with column name similar to RETURNING *  ... it will return a sqlalchemy model 


    return new_post


@router.get("/{id}", response_model=schemas.PostResponse ) #{id} is a path parameter
def get_post(id:int, db: Session = Depends(get_db)):  #fastapi automatically extract id , and pydantic validating it


    post= db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    del_post= db.query(models.Post).filter(models.Post.id == id)




    
    if del_post.first() == None:          # if id did not exist then 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    del_post.delete(synchronize_session=False)
    db.commit()
    

    return Response(status_code=status.HTTP_204_NO_CONTENT)
  
@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):


    post_query = db.query(models.Post).filter(models.Post.id == id)  # for checking wether id exist nor not

    post = post_query.first()
   

    if post == None:  # if not exist then 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False) # since id exists , now updading values via this new query

    db.commit() 



    return post_query.first() # returning query data





