from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import models, schemas


async def select_all_universities(session: AsyncSession) -> List[schemas.University]:
    result = await session.execute(select(models.university))
    return result.all()
