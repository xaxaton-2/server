from typing import List

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import schemas
from src.users import crud
from src.database import get_session


user_router = fastapi.APIRouter()


@user_router.get("/universities", response_model=List[schemas.University])
async def all_universities(session: AsyncSession = fastapi.Depends(get_session)):
    universities = await crud.select_all_universities(session)
    return [
        schemas.University(id=u.id, name=u.name, city=u.city, image=u.image, user_id=u.user_id) for u in universities
    ]


@user_router.get("/faculties", response_model=List[schemas.Faculty])
async def all_faculties(session: AsyncSession = fastapi.Depends(get_session)):
    faculties = await crud.select_all_faculties(session)
    return [
        schemas.Faculty(
            id=f.id, name=f.name,
            university={
                "id": f.university_id,
                "name": f.university_name,
                "image": f.university_image,
                "city": f.university_city,
                "user_id": f.university_user_id
            }) for f in faculties
    ]

# @user_router.post("")

# @router.post("/register/student/", response_model=schemas.StudentCreate, tags=["reg_student"])
# async def register_student(user: schemas.StudentCreate):
#     async with engine.connect() as conn:
#         async_result = await conn.stream(select(models.student))
        
#         async for row in async_result:
#             print("row: %s" % (row,))
#         return user