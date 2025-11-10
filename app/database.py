from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# SQLALCHEMY_DATABASE_URL = '<db_name>://<username>:<password>@<ip-address/hostname>' # format for connecting to a db
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi' # this works in psycopg2 
# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:password@localhost/fastapi'  
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'  

engine= create_engine(SQLALCHEMY_DATABASE_URL) # connects orm to db

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # for executing quries

Base = declarative_base()  # all the model/table will inherit this 

# db connection dependecy
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()