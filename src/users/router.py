from typing import List

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import token, utils
from src.users import schemas
from src.users import crud
from src.database import get_session


user_router = fastapi.APIRouter()


@user_router.get("/universities/", response_model=List[schemas.University])
async def all_universities(session: AsyncSession = fastapi.Depends(get_session)):
    universities = await crud.select_all_universities(session)
    return [
        schemas.University(
            id=u.get("id"),
            name=u.get("name"),
            city=u.get("city"),
            image=u.get("image"),
            score=u.get("score")
        ) for u in universities
    ]


@user_router.get("/faculties/", response_model=List[schemas.FacultyRead])
async def all_faculties(session: AsyncSession = fastapi.Depends(get_session)):
    faculties = await crud.select_all_faculties(session)
    return [
        schemas.FacultyRead(
            id=f.id,
            name=f.name,
            university_id=f.university_id
        ) for f in faculties
    ]


@user_router.post(
    "/faculties/", description="Auth required (add Authorized to header in postman)"
)
async def create_faculty(data: schemas.Faculty, request: fastapi.Request):
    faculty = await crud.create_faculty(data, request)
    if not faculty:
        raise fastapi.HTTPException(status_code=403, detail="Not authorized")
    return faculty


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


@user_router.post(
    "/departments/", description="Auth required (add Authorized to header in postman)"
)
async def create_department(data: schemas.DepartmentCreate, request: fastapi.Request):
    department = await crud.create_department(data, request)
    if not department:
        raise fastapi.HTTPException(status_code=403, detail="Not authorized")
    return department


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

@user_router.post(
    "/groups/", description="Auth required (add Authorized to header in postman)"
)
async def create_group(data: schemas.GroupCreate, request: fastapi.Request):
    group = await crud.create_group(data, request)
    if not group:
        raise fastapi.HTTPException(status_code=403, detail="Not authorized")
    return group


@user_router.post("/register/student/")
async def register_student(data: schemas.StudentWrite):
    student = await crud.register_student(data)
    if student is None:
        raise fastapi.HTTPException(status_code=403, detail="Email exists")
    return student


@user_router.post("/register/university/")
async def register_university(data: schemas.UniversityWrite):
    university = await crud.register_university(data)
    if university is None:
        raise fastapi.HTTPException(status_code=403, detail="Email exists")
    return university


@user_router.post("/login/")
async def login(data: schemas.Login):
    user = await crud.get_user_by_email(data.email)
    if user is None:
        raise fastapi.HTTPException(status_code=403, detail="User does not exist")
    # need to add in prod
    # if user.hashed_password != utils.hash_password(data.password):
    #     raise fastapi.HTTPException(status_code=403, detail="Incorrect pwd")
    profile = await crud.get_user_profile(user.id, user.role)
    response = {
        "token": token.generate_jwt_token(user.id),
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }
    }
    if user.role == 0:
        response["student"] = profile
    elif user.role == 1:
        response["university"] = profile
    elif user.role == 2:
        response["company"] = profile
    return response


@user_router.post("/auth/")
async def auth(data: schemas.Auth):
    user = await crud.get_user_by_token(data.token)
    profile = await crud.get_user_profile(user.id, user.role)
    response = {
        "token": token.generate_jwt_token(user.id),
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }
    }
    if user.role == 0:
        response["student"] = profile
    elif user.role == 1:
        response["university"] = profile
    elif user.role == 2:
        response["company"] = profile
    return response


@user_router.get("/students/")
async def all_students(
    city: str = None, university_id: int = None, faculty_id: int = None,
    course: int = None, department_id: int = None,
    session: AsyncSession = fastapi.Depends(get_session)
):
    students = await crud.get_all_students(
        city=city, u_id=university_id, f_id=faculty_id, course=course, d_id=department_id
    )
    return students


@user_router.get("/students/{id}/")
async def get_student(id: int):
    student = await crud.get_student_by_id(id)
    if not student:
        raise fastapi.HTTPException(status_code=404, detail="Student not found")
    return student
