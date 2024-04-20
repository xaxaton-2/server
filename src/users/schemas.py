from pydantic import BaseModel


class University(BaseModel):
    id: int
    name: str
    city: str
    image: str | None = None
    user_id: int


class Faculty(BaseModel):
    id: int
    name: str
    university: University
