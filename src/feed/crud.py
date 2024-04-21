from typing import List

from src.auth import token as jwt_token

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from src.feed import models as models_feed, schemas as schemas_feed
from src.users import models as models_users, schemas as schemas_users
from src.database import database


async def select_all_posts(session: AsyncSession) -> List[schemas_feed.PostRead]:
    # result = await session.execute(select(models_feed.post))
    massive: List[schemas_feed.PostRead] = []

    query = models_feed.post.select()
    result: List[schemas_feed.Post] = await database.fetch_all(query)
    print(result, query)
    for i in result:
        event_id = i["event_id"]
        student_id = i["student_id"]
        resp = await database.execute(models_feed.event.select().where(models_feed.event.c.id == event_id))
        event_type_id = resp["event_type_id"]
        resp = await database.execute(models_users.student.select().where(models_users.student.c.id == student_id))
        group_id = resp["u_group_id"]
        resp = await database.execute(models_users.group.select().where(models_users.group.c.id == group_id))
        course = resp["course"]
        department_id = resp["department_id"]
        resp = await database.execute(models_users.department.select().where(models_users.department.c.id == department_id))
        faculty_id = resp["faculty_id"]
        resp = await database.execute(models_users.faculty.select().where(models_users.faculty.c.id == faculty_id))
        university_id = resp["university_id"]
        resp = await database.execute(models_users.university.select().where(models_users.university.c.id == university_id))
        city = resp["city"]
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
    return massive
    

async def insert_like_on_post(id: int):
    query = models_feed.post.update().where(models_feed.post.c.id == id).values(likes=models_feed.post.c.likes+1)
    print(query)
    await database.execute(query)

async def get_post(id: int) -> schemas_feed.Post:
    return database.fetch_one(models_feed.post.select().where(models_feed.post.c.id == id))


async def register_post(data: schemas_feed.PostCreate, request: Request):
    header = request.headers.get("Authorization", None)
    if not header:
        return None
    user, _ = await jwt_token.authenticate(header)

    query = models_feed.post.insert().values(
        text=data["text"],
        image=data["image"],
        hashtags=data["hashtags"],
        event_id=data["event_id"],
        student_id=user.id
    )
    await database.execute(query)

async def select_all_events(session: AsyncSession) -> List[schemas_feed.Event]:
    result = await session.execute(select(models_feed.event))
    return result.all()

