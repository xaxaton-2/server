from typing import List

from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import models, schemas


university_cls = aliased(models.university, name="university")
faculty_cls = aliased(models.faculty, name="faculty")


async def select_all_universities(session: AsyncSession) -> List[schemas.University]:
    result = await session.execute(select(models.university))
    return result.all()


async def select_all_faculties(session: AsyncSession) -> List[schemas.Faculty]:
    result = await session.execute(
        select(models.faculty, models.university)
        .join(models.university, models.faculty.c.id == models.university.c.id)
    )
    return result.all()
