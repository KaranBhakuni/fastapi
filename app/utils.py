from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  #specifying which hashing algo we will use

def hash(password: str):
    return pwd_context.hash(password)
    