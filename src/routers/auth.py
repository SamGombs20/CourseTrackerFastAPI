from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import ValidationError
from sqlmodel import select
from schema.user import UserCreate, UserRead
from model.user import User
from auth.jwt_handler import create_access_token, create_refresh_token, decode_token
from auth.utils import verify_password, get_password_hash

from database import get_session
from core.config import settings
from model.token import Token
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data:OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    #Get the credentials
    username = form_data.username
    password = form_data.password

    result = await db.execute(select(User).where(User.username == username))
    user:User = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES)
    access_token = create_access_token(
        user.username, access_token_expires
    )
    refresh_token = create_refresh_token(user.username)

    return{
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }

@router.post("/register", response_model=UserRead)
async def register_user(user_in:UserCreate, session:AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == user_in.username))
    user:User = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        firstName = user_in.firstName,
        lastName = user_in.lastName,
        username = user_in.username,
        hashed_password = hashed_password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token:str= Body(...))->Any:
    try:
        payload = decode_token(refresh_token)
        if "token_type" not in payload or payload["token_type"]!="refresh":
            raise HTTPException (
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate":"Bearer"},
            )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found",
                headers={"WWW-Authenticate":"Bearer"}
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES)
        access_token = create_access_token(
            username, access_token_expires
        )
        new_refresh_token = create_refresh_token(username)
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )
    

