from datetime import datetime
from sqlalchemy import MetaData, Boolean, Integer, \
    String, ForeignKey, TIMESTAMP, Table, Column, VARCHAR, JSON

metadata = MetaData()


role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', VARCHAR(255), nullable=False),
    Column('permissions', JSON),
)

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', VARCHAR(255), nullable=False),
    Column('phone', VARCHAR(50), nullable=True),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
    Column('role_id', Integer, ForeignKey(role.c.id), default=1),

    Column('email', VARCHAR(255), nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False)
)
