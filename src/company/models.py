from sqlalchemy import (
    Table, Column, String, Integer, ForeignKey, MetaData
)

metadata = MetaData()

company = Table(
    "company",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("image", String),
    Column("user_id", Integer, ForeignKey("user.id")),
)

student_like = Table(
    "student_like",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("company_id", Integer, ForeignKey("company.id")),
    Column("student_id", Integer, ForeignKey("student.id"))
)