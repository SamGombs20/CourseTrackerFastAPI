from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from core.config import settings
from jose import jwt

def create_access_token(
        subject:str,expires_delta:Optional[timedelta]=None
)->str:
    #Create JWT access token
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire= datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES)
    
    to_encode={
        "sub":str(subject),
        "exp":expire,
        "iat":datetime.utcnow()
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
def create_refresh_token(subject:str):
    #Create JWT refresh token
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_IN_DAYS)
    to_encode={
        "sub":str(subject),
        "exp":expire,
        "iat":datetime.utcnow()
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token:str)->Dict[str,Any]:
    #Decode token
    payload = jwt.decode(
        token=token,key= settings.SECRET_KEY,algorithms=settings.ALGORITHM
    )
    return payload
