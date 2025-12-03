from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

class CourseBase(SQLModel):
    name: str = Field(index=True)
    category: str = Field(index=True)
    description: str
    status: str = Field(
        default="",
        description="Not Started | In Progress | Completed | ''"
    )
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    rating: Optional[str] = None

class Course(CourseBase, table=True):
    __tablename__ = "courses"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )
class CourseCreate(SQLModel):
    name: str
    category: str
    description: str
    status: Optional[str] = ""
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    rating: Optional[str] = None

class CourseRead(SQLModel):
    id: UUID
    name: str
    category: str
    description: str
    status: Optional[str] = ""
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    rating: Optional[str] = None

class CourseUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    rating: Optional[str] = None