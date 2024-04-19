from typing import List

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import schemas, models
from src.users.crud import select_all_universities
from src.database import engine, get_session


user_router = fastapi.APIRouter()


@user_router.get("/universities", response_model=List[schemas.University])
async def all_universities(session: AsyncSession = fastapi.Depends(get_session)):
    universities = await select_all_universities(session)
    print(universities)
    return [schemas.University(u.id, u.name, u.city, u.image, u.user_id) for u in universities]


# @router.post("/register/student/", response_model=schemas.StudentCreate, tags=["reg_student"])
# async def register_student(user: schemas.StudentCreate):
#     async with engine.connect() as conn:
#         async_result = await conn.stream(select(models.student))
        
#         async for row in async_result:
#             print("row: %s" % (row,))
#         return user