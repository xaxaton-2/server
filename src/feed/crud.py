from typing import List

from src.auth import token as jwt_token

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, HTTPException
from src.feed import models as models_feed, schemas as schemas_feed
from src.users import models as models_users, schemas as schemas_users
from src.database import database


async def select_all_posts(session: AsyncSession) -> List[schemas_feed.PostRead]:
    # result = await session.execute(select(models_feed.post))
    massive: List[schemas_feed.PostRead] = []

    query = models_feed.post.select()
    result: List[schemas_feed.Post] = await database.fetch_all(query)
    for i in result:
        # hello everyone
        event_id = i.event_id
        student_id = i.student_id
        resp = await database.fetch_one(models_feed.event.select().where(models_feed.event.c.id == event_id))
        if resp is None: raise HTTPException(500, "DB is not fully")
        event_type_id = resp.event_type_id
        resp = await database.fetch_one(models_users.student.select().where(models_users.student.c.id == student_id))
        group_id = resp.u_group_id
        resp = await database.fetch_one(models_users.group.select().where(models_users.group.c.id == group_id))
        course = resp.course
        department_id = resp.department_id
        resp = await database.fetch_one(models_users.department.select().where(models_users.department.c.id == department_id))
        faculty_id = resp.faculty_id
        resp = await database.fetch_one(models_users.faculty.select().where(models_users.faculty.c.id == faculty_id))
        university_id = resp.university_id
        resp = await database.fetch_one(models_users.university.select().where(models_users.university.c.id == university_id))
        city = resp.city
        # how are you?
        massive.append(
            schemas_feed.PostRead(
                city=city,
                university_id=university_id,
                faculty_id=faculty_id,
                department_id=department_id,
                group_id=group_id,
                course=course,
                event_id=event_id,
                event_type_id=event_type_id,
                student_id=student_id
            )
        )
    # eto pofiksim
    return massive


async def insert_like_on_post(id: int):
    query = models_feed.post.update().where(models_feed.post.c.id == id).values(likes=models_feed.post.c.likes+1)
    await database.execute(query)

async def get_post(id: int) -> schemas_feed.Post:
    return database.fetch_one(models_feed.post.select().where(models_feed.post.c.id == id))


async def register_post(data: schemas_feed.PostCreate, request: Request):
    header = request.headers.get("Authorization", None)
    if not header:
        return None
    user, _ = await jwt_token.authenticate(header)

    query = models_feed.post.insert().values(
        text=data.text,
        image=data.image,
        hashtags=data.hashtags,
        event_id=data.event_id,
        student_id=user.student_id
    )
    return await database.execute(query)

async def register_event(data: schemas_feed.EventCreate, request: Request):
    header = request.headers.get("Authorization", None)
    if not header:
        return None
    user, _ = await jwt_token.authenticate(header)
    print(user)
    print(user.university_id)
    query = models_feed.event.insert().values(
        university_id=user.university_id,
        name=data.name,
        date=data.date,
        event_type_id=data.event_type_id
    )
    return await database.execute(query)

async def select_all_events(session: AsyncSession) -> List[schemas_feed.Event]:
    result = await session.execute(select(models_feed.event))
    return result.all()
