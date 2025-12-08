from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime

from schema.link import UserCourseLink
from schema.course import Course
from schema.user import UserBase





class User(UserBase, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    courses:List["Course"] = Relationship(back_populates="users", link_model=UserCourseLink)


class UserLogIn(BaseModel):
    username:str
    password:str


class UserPublic(BaseModel):
    id: UUID
    firstName: str
    lastName: str
    username: str
    created_at: datetime

