from pydantic import BaseModel


class University(BaseModel):
    id: int
    name: str
    city: str
    image: str = None
    user_id: int
 