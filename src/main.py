from typing import List
from uuid import uuid4
from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from auth.utils import get_password_hash
from core.config import settings
from routers import auth, users


import uvicorn

from model.course import Course, CourseCreate, CourseRead
from model.user import User, UserCreate, UserRead
from database import get_session, init_db

# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     await init_db()
#     yield

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# class Course(BaseModel):
#     id:str
#     name:str
#     category:str
#     description:str
#     status:Optional[str]=""
#     startDate:Optional[str]=None
#     endDate:Optional[str]=None
#     rating: Optional[str] = None
# class SavePayload(BaseModel):
#     courses:List[Course]

# courses:List[Course] =[]
@app.on_event("startup")
async def start_up():
    await init_db()

app.include_router(auth.router)
app.include_router(users.router,prefix=settings.API_V1_STR)
@app.get("/")
async def root():
    return {"message":"Course tracker backend running!"}
# @app.post("/save")
# async def save(payload:SavePayload):
#     global courses
#     courses = payload.courses
#     print(payload.courses)
#     return {"status":"success"}

# @app.get("/load")
# async def load():
#     return {"courses":courses}
@app.get("/courses",response_model=List[CourseRead])
async def get_courses(session:AsyncSession=Depends(get_session)):
    result = await session.execute(select(Course))
    courses = result.scalars().all()
    return courses
@app.post("/addCourse", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_course(course_in:CourseCreate, session:AsyncSession=Depends(get_session)):
   
    course = Course(
        name=course_in.name,
        category=course_in.category,
        description=course_in.description,
        status=course_in.status,
        startDate=course_in.startDate,
        endDate=course_in.endDate,
        rating=course_in.rating
    )
    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course
@app.put("/updateCourse/{course_id}", response_model=CourseRead)
async def update_course(course_id:str, course_in:CourseCreate, session:AsyncSession= Depends(get_session)):
    result = await session.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
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
@app.delete("/deleteCourse/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id:str, session:AsyncSession=Depends(get_session)):
    result = await session.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    await session.delete(course)
    await session.commit()
    return
@app.post("/addUser", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(get_session)):

    # Check duplicate
    result = await session.execute(
        select(User).where(User.username == user_in.username)
    )
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user_in.password)
    
    user = User(
        firstName=user_in.firstName,
        lastName=user_in.lastName,
        username=user_in.username,
        hashed_password=hashed_password
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

if __name__ == "__main__": 
    uvicorn.run("main:app", host="127.0.0.1", port=4000, reload=True)