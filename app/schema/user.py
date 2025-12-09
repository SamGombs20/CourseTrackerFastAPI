from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import Field
from sqlmodel import  Relationship, SQLModel



class UserCreate(SQLModel):
    firstName: str
    lastName: str
    username: str
    password: str
    
class UserBase(SQLModel):
    firstName: str = Field(index=True)
    lastName: str = Field(index=True)
    username: str = Field(index=True, unique=True)


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
