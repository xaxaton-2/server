from typing import Optional

from pydantic import BaseModel


class University(BaseModel):
    id: int
    name: str
    city: str
    image: Optional[str] = None


class Faculty(BaseModel):
    id: int
    name: str
    university_id: int


class Department(BaseModel):
    id: int
    name: str
    faculty_id: int


class Group(BaseModel):
    id: int
    name: str
    course: int = 1
    department_id: int


class Student(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: Optional[str] = None
    group_id: int
    image: Optional[str] = None


class StudentWrite(Student):
    password: str


class StudentRead(Student):
    id: int
    score: int | None = 0
