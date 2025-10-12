from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):  # api ka schema ( datatype ) 
    title: str
    content: str

#order of calling:1st method matched then r2 out match

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/createpost")
def create_posts(payload: dict = Body(...)):    #body sare feilds ko nikal ke payload mai daal dega ye
    print(payload)
    # return {"message": "succesfully created posts"}
    return {"new_post": f"title{payload['title']} content{payload['content']}"}

@app.post("/createposts")
def create_posts(payload: Post):    # data validation Post class se 
    print(payload.title)
    # return {"message": "succesfully created posts"}
    return {"new_post": "received"}