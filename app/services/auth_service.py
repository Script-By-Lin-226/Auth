from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError
from app.api.v1 import auth
from datetime import datetime, timedelta
from app.core.config import settings

#GET ENV
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

# CREATE ACCESS TOKEN AND REFRESH_ACCESS TOKEN
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type":"access"})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,  algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type":"refresh"})
    refresh_token = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token

# DECODE TOKEN
def decode_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )

