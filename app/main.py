from fastapi import FastAPI
from .database import engine   # engine establish connection btw db and orm 
from . import models
from .routers import posts, user, auth
from .config import settings

print(settings.database_username)

models.Base.metadata.create_all(bind=engine)  # check model and if not created in db then create them, it not update them if we alter any column



app = FastAPI()

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}





