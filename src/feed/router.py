from typing import List

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import token, utils
from src.feed import schemas
from src.feed import crud
from src.database import get_session


feed_router = fastapi.APIRouter()

@feed_router.get("/posts/", response_model=List[schemas.PostRead])
async def all_posts(session: AsyncSession = fastapi.Depends(get_session)):
    posts = await crud.select_all_posts(session)
    return posts