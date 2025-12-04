from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import select

from database import get_session
from auth.jwt_bearer import get_current_user
from model.user import User
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter(prefix="/users", tags=["users"])
@router.get("/me", response_model=User)
async def read_user(current_user:str = Depends(get_current_user),
                    session:AsyncSession = Depends(get_session)):
    result = session.execute(select(User).where(User.username == current_user))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail ="User not found"
        )
    return user
