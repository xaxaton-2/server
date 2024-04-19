from typing import Optional
from pydantic import BaseModel

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    email: str

    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str

    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class StudentRead(BaseModel):
    name: str
    surname: str
    patronymic: str = None
    score: int = 0
    user: UserRead
    image: str = None


class StudentCreate(StudentRead):
    user: UserCreate
