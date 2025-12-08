from uuid import UUID
from sqlmodel import Field, SQLModel


class UserCourseLink(SQLModel, table=True):
    __tablename__="user_course_link"
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    course_id: UUID = Field(foreign_key="courses.id", primary_key=True)
