from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import models, schemas


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


async def get_student(email: str, session: AsyncSession) -> schemas.StudentRead:
    result = await session.execute(
        select(models.student).where(models.student.c.email == email)
    )
    return result


async def register_student(data: schemas.StudentWrite, session: AsyncSession):
    student = await get_student(data.email, session)
    print(student)
