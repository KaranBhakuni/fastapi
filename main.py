from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/createpost")
def create_posts(payload: dict = Body(...)):    #body sare feilds ko nikal ke payload mai daal dega ye
    print(payload)
    # return {"message": "succesfully created posts"}
    return {"new_post": f"title{payload['title']} content{payload['content']}"}
