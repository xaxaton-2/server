from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import utils
from src.users import models, schemas
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
        user_id=user,
        u_group_id=data.group_id,
    )
    student = await database.execute(query)

    return {**data.dict(), "student_id": student}


async def get_university(email: str) -> schemas.UniversityRead:
    query = models.user.select().where(models.user.c.email == email)
    u = await database.fetch_one(query)
    if u:
        print(u.email, u.id)
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
