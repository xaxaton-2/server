from sqlalchemy import (
    Table, Column, String, Integer, ForeignKey, MetaData
)

from src.users import models


metadata = MetaData()

company = Table(
    "company",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("image", String),
    Column("user_id", Integer, ForeignKey(models.user.c.id)),
)

student_like = Table(
    "student_like",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("company_id", Integer, ForeignKey("company.id")),
    Column("student_id", Integer, ForeignKey(models.user.c.id))
)
