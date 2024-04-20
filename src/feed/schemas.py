from typing import List, Optional, Text
from datetime import datetime
from pydantic import BaseModel
# from src.users.schemas import (
#     University, Student, Department, Faculty, Group,
#     StudentRead
# )

class EventType(BaseModel):
    id: int
    name: str
    score: int

class Event(BaseModel):
    id: int
    name: str
    date: datetime
    event_type_id: int # EventType.id
    university_id: int # University.id


class EventRequest(BaseModel):
    id: int
    status: List[str] = ["pending", "accepted", "denied"]
    event_id: int # Event.id
    student_id: int # StudentRead.id

class Post(BaseModel):
    id: int
    student_id: int #  StudentRead.id
    text: Text
    image: Optional[str]
    hashtags: Optional[str] = "Вуз, Волонтеры, математика"
    event_id: Optional[int]
    likes: int

class PostComment(BaseModel):
    id: int
    text: Text
    student_id: int # StudentRead.id
    post_id: int # Post.id

class PostLike(BaseModel):
    id: int
    student_id: int # StudentRead.id
    post_id: int # Post.id

class EventCreate(BaseModel):
    name: str # Event.name
    date: datetime # Event.date
    event_type_id: int # Event.event_type_id

class EventRequestCreate(BaseModel):
    event_id: int # EventRequest.event_id

class PostCreate(BaseModel):
    text: Text # Post.text
    image: str # Post.image
    hashtags: str # Post.hashtags
    event_id: int # Post.event_id

class PostRead(BaseModel):
    city: str # University.city
    university_id: int # Faculty.university_id
    faculty_id: int # Department.faculty_id
    department_id: int # Group.department_id
    group_id: int # Student.group_id
    course: int # Group.course
    event_id: int # Post.event_id
    event_type_id: int # Event.event_type_id
    student_id: int # Post.student_id

    def __init__(
            self,
            city,
            university_id,
            faculty_id,
            department_id,
            group_id,
            course,
            event_id,
            event_type_id,
            student_id
    ) -> None:
        self.city = city
        self.university_id = university_id
        self.faculty_id = faculty_id
        self.department_id = department_id
        self.group_id = group_id
        self.course = course
        self.event_id = event_id
        self.event_type_id = event_type_id
        self.student_id = student_id