import os
import secrets
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class Settings(BaseSettings):
    API_V1_STR:str ="/api/v1"
    #Security settings
    SECRET_KEY:str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_IN_MINUTES:int = 30
    REFRESH_TOKEN_EXPIRE_IN_DAYS:int=7
    ALGORITHM:str = "HS256"

settings = Settings()
