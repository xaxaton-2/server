from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.feed import models as models_feed, schemas as schemas_feed
from src.users import models as models_users, schemas as schemas_users
from src.database import database


async def select_all_posts(session: AsyncSession) -> List[schemas_feed.PostRead]:
    result = await session.execute(select(models_feed.post))
    massive: List[schemas_feed.PostRead] = []
    for i in result.all():
        pass
    

async def select_all_events(session: AsyncSession) -> List[schemas_feed.Event]:
    result = await session.execute(select(models_feed.event))
    return result.all()

