from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session # this Session will be used in routs, to access db
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db # engine establish connection btw db and orm 
from sqlalchemy import func

router=APIRouter( prefix="/posts",   #
                 tags=['Posts'])    # all the api will come under Posts section


# domain/route?1st_query&2nd_query_para  dont use string in search para // use %20 for space

# @router.get("/", response_model=List[schemas.PostResponse])  # to get list of post, we will need List from typing
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0 , search:Optional[str]=""):

    # filter query based on query parameter
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # return posts  #fastapi will automatically serialize my list to json
    # join with out filters
    # results= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id== models.Post.id, isouter=True).group_by(models.Post.id).all()
    results= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id== models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return [{"Post": post, "votes": votes} for post, votes in results]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
 
    # print(post.model_dump())
    # print(current_user.email)
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) # unpacking list (**) ... since schema match with db 
    db.add(new_post)  #execute query
    db.commit()
    db.refresh(new_post) # returing the value with column name similar to RETURNING *  ... it will return a sqlalchemy model 


    return new_post


@router.get("/{id}", response_model=schemas.PostOut) #{id} is a path parameter
def get_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):  #fastapi automatically extract id , and pydantic validating it


    # post= db.query(models.Post).filter(models.Post.id == id).first()
    # post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id== models.Post.id, isouter=True).group_by(models.Post.id).all().filter(models.Post.id == id).first()
    post = (

        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.id == id)       # move filter here
        .group_by(models.Post.id)
        .first()                            # returns a single record
    )

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if post.owner_id != current_user.id:  # compare owner_id
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):


    post_query = db.query(models.Post).filter(models.Post.id == id)  # for checking wether id exist nor not

    post = post_query.first()
   

    if post == None:  # if not exist then 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    if post.owner_id != current_user.id:                   #check to insure that user can edit his post only
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not Authorized to perform the request")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False) # since id exists , now updading values via this new query

    db.commit() 



    return post_query.first() # returning query data





