from sqlalchemy import (
    Integer, String, Table, Column,
    MetaData, ForeignKey, TIMESTAMP, Text
)
from datetime import datetime

from src.users import models


metadata = MetaData()

# ----------------events ----------------

event_type = Table(
    'event_type',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String),
    Column('score', Integer),
)

event = Table(
    'event',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String),
    Column('date', TIMESTAMP, default=datetime.utcnow),
    Column('event_type_id', Integer, ForeignKey('event_type.id')),
    Column('university_id', Integer, ForeignKey(models.university.c.id))
)

event_request = Table(
    'event_request',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('status', String),
    Column("event_id", Integer, ForeignKey('event.id')),
    Column("student_id", Integer, ForeignKey(models.student.c.id))
)
# ----------------- posts -----------------

post = Table(
    "post",
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column("student_id", Integer, ForeignKey(models.student.c.id)),
    Column("text", Text),
    Column("image", String),
    Column("hashtags", String),
    Column("event_id", Integer, ForeignKey("event.id")),
    Column("likes", Integer)
)

post_like = Table(
    "post_like",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("student_id", Integer, ForeignKey(models.student.c.id)),
    Column("post_id", Integer, ForeignKey("post.id"))
)

post_comment = Table(
    "post_comment",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("text", Text),
    Column("student_id", Integer, ForeignKey(models.student.c.id)),
    Column("post_id", Integer, ForeignKey("post.id"))
)
