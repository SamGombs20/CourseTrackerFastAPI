from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime


class UserBase(SQLModel):
    firstName: str = Field(index=True)
    lastName: str = Field(index=True)
    username: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserLogIn(BaseModel):
    username:str
    password:str

class UserCreate(SQLModel):
    firstName: str
    lastName: str
    username: str
    password: str
class UserPublic(BaseModel):
    id: UUID
    firstName: str
    lastName: str
    username: str
    created_at: datetime

class UserRead(SQLModel):
    id: UUID
    firstName: str
    lastName: str
    username: str
    created_at: datetime


class UserUpdate(SQLModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: Optional[str] = None
