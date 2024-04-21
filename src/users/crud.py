from typing import List

from fastapi import Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import utils, token as jwt_token
from src.users import models, schemas
from src.company import models as c_models
from src.database import database


async def select_all_universities(session: AsyncSession) -> List[schemas.University]:
    result = await session.execute(select(models.university))
    return result.all()


async def select_all_faculties(session: AsyncSession) -> List[schemas.Faculty]:
    result = await session.execute(select(models.faculty))
    return result.all()


async def select_all_departments(session: AsyncSession) -> List[schemas.Department]:
    result = await session.execute(select(models.department))
    return result.all()


async def select_all_groups(session: AsyncSession) -> List[schemas.Group]:
    result = await session.execute(select(models.group))
    return result.all()


async def get_student(email: str) -> schemas.StudentRead:
    query = models.user.select().where(models.user.c.email == email)
    u = await database.fetch_one(query)
    if u:
        query = models.student.select().where(models.student.c.user_id == u.id)
        student = await database.fetch_one(query)
        if not student:
            return None
        return schemas.StudentRead(
            id=student["id"], email=u["email"],
            name=student["name"], surname=student["surname"],
            patronymic=student["patronymic"], group_id=student["u_group_id"],
            image=student["image"], score=student["score"]
        )
    else:
        return None


async def get_student_by_id(id: int) -> schemas.StudentRead:
    query = models.student.select().where(models.student.c.id == id)
    student = await database.fetch_one(query)
    if not student:
        return None
    query = models.user.select().where(models.user.c.id == student.user_id)
    user = await database.fetch_one(query)
    return schemas.StudentRead(
        id=student["id"], email=user["email"],
        name=student["name"], surname=student["surname"],
        patronymic=student["patronymic"], group_id=student["u_group_id"],
        image=student["image"], score=student["score"]
    )

async def get_all_students(**kwargs) -> List[schemas.StudentRead]:
    query = (
        select(
            models.student, models.user,
            models.group, models.university,
            models.department, models.faculty
        )
        .join(models.user, models.student.c.user_id == models.user.c.id)
        .join(models.group, models.student.c.u_group_id == models.group.c.id)
        .join(models.department, models.group.c.department_id == models.department.c.id)
        .join(models.faculty, models.department.c.faculty_id == models.faculty.c.id)
        .join(models.university, models.faculty.c.university_id == models.university.c.id)
        .order_by(models.student.c.score.desc())
    )
    if kwargs["city"]:
        query = query.filter(models.university.c.city == kwargs["city"].title())
    if kwargs["u_id"]:
        query = query.filter(models.university.c.id == kwargs["u_id"])
    if kwargs["f_id"]:
        query = query.filter(models.faculty.c.id == kwargs["f_id"])
    if kwargs["course"]:
        query = query.filter(models.group.c.course == kwargs["course"])
    if kwargs["d_id"]:
        query = query.filter(models.department.c.id == kwargs["d_id"])
    students = await database.fetch_all(query)
    return [schemas.StudentRead(
        id=student["id"], email=student["email"],
        name=student["name"], surname=student["surname"],
        patronymic=student["patronymic"], group_id=student["u_group_id"],
        image=student["image"], score=student["score"]
    ) for student in students
    ]


async def register_student(data: schemas.StudentWrite):
    student = await get_student(data.email)
    if student is not None:
        return None
    query = models.user.insert().values(
            email=data.email,
            hashed_password=utils.hash_password(data.password),
            role=0, is_active=True,
            is_superuser=False,
            is_verified=True
        )
    user = await database.execute(query)
    query = models.student.insert().values(
        name=data.name,
        surname=data.surname,
        patronymic=data.patronymic,
        image=data.image,
        score=0,
        user_id=user,
        u_group_id=data.group_id,
    )
    student = await database.execute(query)

    return {**data.dict(), "student_id": student}


async def get_university(email: str) -> schemas.UniversityRead:
    query = models.user.select().where(models.user.c.email == email)
    u = await database.fetch_one(query)
    if u:
        query = models.university.select().where(models.university.c.user_id == u.id)
        university = await database.fetch_one(query)
        if not university:
            return "exist"
        return schemas.UniversityRead(
            email=u["email"], name=university["name"],
            city=university["city"], image=university["image"],
            user_id=university["user_id"]
        )
    else:
        return None


async def register_university(data: schemas.UniversityWrite):
    university = await get_university(data.email)
    if university is not None:
        return None
    query = models.user.insert().values(
            email=data.email,
            hashed_password=utils.hash_password(data.password),
            role=1, is_active=True,
            is_superuser=False,
            is_verified=True
        )
    user = await database.execute(query)
    query = models.university.insert().values(
        name=data.name,
        city=data.city,
        image=data.image,
        user_id=user,
    )
    university = await database.execute(query)

    return {**data.dict(), "university_id": university}


async def get_user_by_id(id: int):
    query = models.user.select().where(models.user.c.id == id)
    user = await database.fetch_one(query)
    if user is None:
        return None
    return user


async def get_user_by_email(email: str):
    query = models.user.select().where(models.user.c.email == email)
    user = await database.fetch_one(query)
    if user is None:
        return None
    return user


async def create_faculty(data: schemas.Faculty, request: Request):
    header = request.headers.get("Authorization", None)
    if not header:
        return None
    user, _ = await jwt_token.authenticate(header)

    query = models.university.select().where(models.university.c.user_id == user.id)
    university = await database.fetch_one(query)

    if not university:
        raise HTTPException(status_code=403, detail="No root")

    query = models.faculty.insert().values(
        name=data.name, university_id=university.id
    )
    new_faculty = await database.execute(query)

    return {**data.dict(), "faculty_id": new_faculty}


async def create_department(data: schemas.DepartmentCreate, request: Request):
    header = request.headers.get("Authorization", None)
    if not header:
        return None
    user, _ = await jwt_token.authenticate(header)

    query = models.department.insert().values(
        name=data.name, faculty_id=data.faculty_id
    )
    new_department = await database.execute(query)

    return {**data.dict(), "department_id": new_department}


async def get_user_by_token(token: str):
    user, _ = await jwt_token.authenticate(token)
    return user


async def create_group(data: schemas.GroupCreate, request: Request):
    header = request.headers.get("Authorization", None)
    if not header:
        return None
    user, _ = await jwt_token.authenticate(header)

    query = models.group.insert().values(
        name=data.name, course=data.course, department_id=data.department_id
    )
    new_group = await database.execute(query)

    return {**data.dict(), "group_id": new_group}


async def get_user_profile(id: int, role: int):
    if role == 0:
        query = models.student.select().where(models.student.c.user_id == id)
    elif role == 1:
        query = models.university.select().where(models.university.c.user_id == id)
    elif role == 2:
        query = c_models.company.select().where(c_models.company.c.user_id == id)
    else:
        return None
    profile = await database.fetch_one(query)
    return profile
