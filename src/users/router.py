from typing import List

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import schemas
from src.users import crud
from src.database import get_session


user_router = fastapi.APIRouter()


@user_router.get("/universities/", response_model=List[schemas.University])
async def all_universities(session: AsyncSession = fastapi.Depends(get_session)):
    universities = await crud.select_all_universities(session)
    return [
        schemas.University(
            id=u.id,
            name=u.name,
            city=u.city,
            image=u.image,
        ) for u in universities
    ]


@user_router.get("/faculties/", response_model=List[schemas.Faculty])
async def all_faculties(session: AsyncSession = fastapi.Depends(get_session)):
    faculties = await crud.select_all_faculties(session)
    return [
        schemas.Faculty(
            id=f.id,
            name=f.name,
            university_id=f.university_id
        ) for f in faculties
    ]


@user_router.get("/departments/", response_model=List[schemas.Department])
async def all_departmenst(session: AsyncSession = fastapi.Depends(get_session)):
    departments = await crud.select_all_departments(session)
    return [
        schemas.Department(
            id=d.id,
            name=d.name,
            faculty_id=d.faculty_id
            ) for d in departments
    ]


@user_router.get("/groups/", response_model=List[schemas.Group])
async def all_groups(session: AsyncSession = fastapi.Depends(get_session)):
    groups = await crud.select_all_groups(session)
    return [
        schemas.Group(
            id=g.id,
            name=g.name,
            course=g.course,
            department_id=g.department_id
            ) for g in groups
    ]


@user_router.post("/register/student/")
async def register_student(
    data: schemas.StudentWrite,
):
    student = await crud.register_student(data)
    if student is None:
        raise fastapi.HTTPException(status_code=403, detail="Email exists")
    return student
