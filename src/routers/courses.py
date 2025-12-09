from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import select

from schema.link import UserCourseLink
from model.user import User
from auth.jwt_bearer import get_current_user
from schema.user import UserRead
from schema.course import Course, CourseCreate, CourseRead
from database import get_session
from routers.users import read_user
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter(prefix="/me", tags=["courses"])
@router.get("/courses", response_model=List[CourseRead])
async def read_user_courses(current_user:str= Depends(get_current_user),session:AsyncSession = Depends(get_session)):
    
    user_result  = await session.execute(
        select(User).where(User.username==current_user)
    )
    user:User = user_result.scalars().first()
    
    result = await session.execute(
        select(Course)
        .join(UserCourseLink)
        .where(UserCourseLink.user_id == user.id)
    )
    
    courses = result.scalars().all()
    return courses
  

@router.post("/addCourse", response_model=CourseRead)
async def add_course(course_in:CourseCreate, current_user:str= Depends(get_current_user), session:AsyncSession=Depends(get_session)):
    user_result  = await session.execute(
        select(User).where(User.username==current_user)
    )
    user:User = user_result.scalars().first()
    course = Course(
        name=course_in.name,
        category=course_in.category,
        description=course_in.description,
        status=course_in.status,
        startDate=course_in.startDate,
        endDate=course_in.endDate,
        rating=course_in.rating
    )
    course.users.append(user)
    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course

@router.put("/updateCourse/{course_id}", response_model=CourseRead)
async def update_course(course_in:CourseRead, current_user:str= Depends(get_current_user),
                        session:AsyncSession= Depends(get_session)):
    user_result = await session.execute(
        select(User).where(User.username==current_user)
    )
    user:User = user_result.scalars().first()
    course_result = await session.execute(
        select(Course).where(Course.id == course_in.id)
    )
    course:Course = course_result.scalars().first()
    course.name = course_in.name
    course.category = course_in.category
    course.description = course_in.description
    course.status = course_in.status
    course.startDate = course_in.startDate
    course.endDate = course_in.endDate
    course.rating = course_in.rating
    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course

@router.delete("/deleteCourse/{course_id}")
async def delete_course(course_id:str, current_user:str= Depends(get_current_user),
                        session:AsyncSession = Depends(get_session)):
    user_result = await session.execute(
        select(User).where(User.username==current_user)
    )
    user:User = user_result.scalars().first()
    course_result = await session.execute(
        select(Course).where(Course.id == course_id)
    )
    course:Course = course_result.scalars().first()
    await session.delete(course)
    await session.commit()
    return {"detail":"Course deleted successfully"}