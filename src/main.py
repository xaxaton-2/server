import fastapi

from src.users.router import user_router
from src.company.router import company_router


app = fastapi.FastAPI(title="LifeCour$e")


app.include_router(user_router)
app.include_router(company_router)
