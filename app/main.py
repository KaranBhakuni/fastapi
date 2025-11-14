from fastapi import FastAPI
from .database import engine   # engine establish connection btw db and orm 
from . import models
from .routers import posts, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_username)

# now we are using alembic
# models.Base.metadata.create_all(bind=engine)  # check model and if not created in db then create them, it not update them if we alter any column



app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origns=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}





