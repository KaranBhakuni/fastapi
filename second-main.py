#CURD WITH RAW DB QUERY

from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
# from psycopg.extars import RealDictCursor
from psycopg.rows import dict_row
import time



#      how to connect via psycopg new version 3
# Connect to your PostgreSQL database
# conn = psycopg.connect(
#     dbname="your_db_name",
#     user="your_username",
#     password="your_password",
#     host="localhost",
#     port="5432",   # default PostgreSQL port
#     cursor_factory=RealDictCursor
# )

# Create a cursor
# cur = conn.cursor()

# # Execute a query
# cur.execute("SELECT version();")

# # Fetch one result
# record = cur.fetchone()
# print("PostgreSQL version:", record)

# # Close the cursor and connection
# cur.close()
# conn.close()


app = FastAPI()

class Post(BaseModel):  # api ka schema ( datatype ) 
    title: str
    content: str
    published: bool = True # defalut value is True even if your doesnt provide
   


while True:

    try:
        # Connect to your PostgreSQL database
        conn = psycopg.connect(
            dbname="fastapi",
            user="postgres",
            password="password",
            host="localhost",
            port="5432",
            row_factory=dict_row    # give values with column name in a dict
        )
        cursor = conn.cursor()
        print("sucessfully connected to db")
        break
    except Exception as error:
        print("db connection failed")
        print("error: ", error)
        time.sleep(2)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/createposts")
def create_posts(payload: Post):    
    print(payload) # pydantic model 
    # print(payload.dict()) dict is deprecated , so use dump_dict()
    print(payload.model_dump()) 
    print(payload.dict())
    print(payload.title)
    # return {"message": "succesfully created posts"}
    return {"new_post": payload}

#CRUD


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts= cursor.fetchall()
    print(posts)
    return {"data": posts}  #fastapi will automatically serialize my list to json

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # cursor.execute(f"INSERT INTO posts (title, content, published)  VALUES({post.title},{post.content},{post.published})") this is wrong method, it can lead to sql injection

    cursor.execute("""INSERT INTO posts (title, content, published)  VALUES(%s,%s,%s) RETURNING * """, (post.title,post.content,post.published))
    new_post= cursor.fetchone()
    conn.commit()

    return {"data": new_post}


@app.get("/posts/{id}") #{id} is a path parameter
def get_post(id:int):  #fastapi automatically extract id , and pydantic validating it
    cursor.execute("""SELECT * FROM posts WHERE id = %s RETURNING *""", (str(id),) )
    post = cursor.fetchone()
    conn.commit()
    # print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        
    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""" , (str(id),))
    del_post = cursor.fetchone()
    conn.commit()

    
    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    # return{'message':f"post is deleted with id {id}"} do not return data while deleting 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""" , (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
   

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")



    return {"data": updated_post}


# fast api have two types of built in docs 
# http://127.0.0.1:8000/docs 
# http://127.0.0.1:8000/redoc 