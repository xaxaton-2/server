from typing import List, Optional, Text
from datetime import datetime
from pydantic import BaseModel
from src.users.schemas import (
    University, Student, Department, Faculty, Group,
    StudentRead
)

class EventType(BaseModel):
    id: int
    name: str
    score: int

class Event(BaseModel):
    id: int
    name: str
    date: datetime
    event_type_id: EventType.id
    university_id: University.id


class EventRequest(BaseModel):
    id: int
    status: List[str] = ["pending", "accepted", "denied"]
    event_id: Event.id
    student_id: StudentRead.id

class Post(BaseModel):
    id: int
    student_id: StudentRead.id
    text: Text
    image: Optional[str]
    hashtags: Optional[str] = "Вуз, Волонтеры, математика"
    event_id: Optional[int]
    likes: int

class PostComment(BaseModel):
    id: int
    text: Text
    student_id: StudentRead.id
    post_id: Post.id

class PostLike(BaseModel):
    id: int
    student_id: StudentRead.id
    post_id: Post.id

class EventCreate(BaseModel):
    name: Event.name
    date: Event.date
    event_type_id: Event.event_type_id

class EventRequestCreate(BaseModel):
    event_id: EventRequest.event_id

class PostCreate(BaseModel):
    text: Post.text
    image: Post.image
    hashtags: Post.hashtags
    event_id: Post.event_id

class PostRead(BaseModel):
    city: University.city
    university_id: Faculty.university_id
    faculty_id: Department.faculty_id
    department_id: Group.department_id
    group_id: Student.group_id
    course: Group.course
    event_id: Post.event_id
    event_type_id: Event.event_type_id
    student_id: Post.student_id