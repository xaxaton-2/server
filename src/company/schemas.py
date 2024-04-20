from typing import Optional

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    image: Optional[str] = None
    email: str
    password: str


class CompanyRead(BaseModel):
    name: str
    image: Optional[str] = None
    email: str
    user_id: int
