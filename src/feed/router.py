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

@feed_router.post("/posts/{id}/likes", response_model=schemas.Post)
async def add_likes(id: int):
    await crud.insert_like_on_post(id)
    post = await crud.get_post(id)
    return post

@feed_router.post("/posts/")
async def add_post(data: schemas.PostCreate, request: fastapi.Request):
    await crud.register_post(data, request)
    return {"status": "success"}