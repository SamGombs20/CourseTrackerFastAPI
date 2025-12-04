from datetime import datetime
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from model.token import TokenPayload
from auth.jwt_handler import decode_token
from core.config import settings
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)
def get_current_user(token:str=Depends(oauth2_scheme))->str:
    #Validates token and return the username
    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)
        #Check for token expiration
        if datetime.fromtimestamp(token_data.exp)<datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate":"Bearer"}
            )
        return token_data.sub
    except(JWTError,ValidationError):
        
        # raise HTTPException(
        #     status_code=status.HTTP_403_FORBIDDEN,
        #     detail="Could not validate the credentials",
        #     headers={"WWW-Authenticate":"Bearer"}
        # )
        raise JWTError()