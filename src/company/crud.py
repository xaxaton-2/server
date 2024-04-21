from src.auth import utils
from src.users import models as u_models
from src.company import models as c_models, schemas
from src.database import database


async def get_company(email: str) -> schemas.CompanyRead:
    query = u_models.user.select().where(u_models.user.c.email == email)
    u = await database.fetch_one(query)
    if u:
        query = c_models.company.select().where(c_models.company.c.user_id == u.id)
        company = await database.fetch_one(query)
        if not company:
            return "exist"
        return schemas.CompanyRead(
            email=u["email"],
            name=company["name"],
            image=company["image"],
            user_id=company["user_id"]
        )
    else:
        return None


async def register_company(data: schemas.CompanyCreate):
    company = await get_company(data.email)
    if company is not None:
        return None
    query = u_models.user.insert().values(
            email=data.email,
            hashed_password=utils.hash_password(data.password),
            role=2, is_active=True,
            is_superuser=False,
            is_verified=True
        )
    user = await database.execute(query)
    query = c_models.company.insert().values(
        name=data.name,
        image=data.image,
        user_id=user
    )
    company = await database.execute(query)

    return {**data.dict(), "company_id": company}
