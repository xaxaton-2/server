from sqlalchemy import MetaData, Integer, Table, String, Boolean, Column, ForeignKey

metadata = MetaData()

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String, unique=True, nullable=False),
    Column('hashed_password', String, nullable=False),

    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False)
)

student = Table(
    'student',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('surname', String, nullable=False),
    Column('patronymic', String, nullable=True),
    Column('score', Integer),
    Column('image', String, nullable=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)

group = Table(
    'group',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String),
    Column('course', String),
    Column('department_id', Integer, ForeignKey('department.id'))
)

department = Table(
    'department',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String),
    Column('faculty_id', Integer, ForeignKey('faculty.id'))
)

faculty = Table(
    'faculty',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String),
    Column('university_id', Integer, ForeignKey('university.id'))
)

university = Table(
    'university',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String),
    Column('image', String, nullable=True),
    Column('user_id', Integer, ForeignKey('user.id'))
)
