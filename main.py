from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):  # api ka schema ( datatype ) 
    title: str
    content: str
    published: bool = True # defalut value is True even if your doesnt provide
    rating: Optional[int]= None # completly optional feild, stores None if not provided

#order of calling:check 1st method matched then r2 out match

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/createpost")
def create_posts(payload: dict = Body(...)):    #body sare feilds ko nikal ke payload mai daal dega ye
    print(payload)
    # return {"message": "succesfully created posts"}
    return {"new_post": f"title{payload['title']} content{payload['content']}"}

@app.post("/createposts")
def create_posts(payload: Post):    # data validation Post class se  or payload ak ek pydantic model hai 
    print(payload) # pydantic model 
    # print(payload.dict()) dict is deprecated , so use dump_dict()
    print(payload.model_dump()) 
    print(payload.dict())
    print(payload.title)
    # return {"message": "succesfully created posts"}
    return {"new_post": payload}

#CRUD
my_posts = [{"title": "post 1", "content": "content of post 1", "id":1},{ 
            "title": "post 2", "content": "content of post 2", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/posts")
def get_posts():
    return {"data": my_posts}  #fastapi will automatically serialize my list to json

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# @app.get("/posts/{id}") #{id} is a path parameter
# def get_post(id:int,response: Response):  #fastapi automatically extract id , and pydantic validating it
#     post = find_post(id)
#     if not post:
#         # response.status_code=404
#         # response.status_code=status.HTTP_404_NOT_FOUND
#         # return{'message': f"post with id: {id} was not found"}
#         
        
#     return{"post_detail": post}

@app.get("/posts/{id}") #{id} is a path parameter
def get_post(id:int):  #fastapi automatically extract id , and pydantic validating it
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        
    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    my_posts.pop(index)
    # return{'message':f"post is deleted with id {id}"} do not return data while deleting 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    post_dict= post.model_dump()
    post_dict['id']=id
    my_posts[index]= post_dict


    return {"data": post_dict}


# fast api have two types of built in docs 
# http://127.0.0.1:8000/docs 
# http://127.0.0.1:8000/redoc 