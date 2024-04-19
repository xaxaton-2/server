from sqlalchemy import (
    Table, Column, String, Integer, ForeignKey, MetaData
)
from src.auth.models import user, student

metadata = MetaData()

company = Table(
    "company",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("image", String),
    Column("user_id", Integer, ForeignKey(user.c.id)),
)

student_like = Table(
    "student_like",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("company_id", Integer, ForeignKey(company.c.id)),
    Column("student_id", Integer, ForeignKey(student.c.id))
)