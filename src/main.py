import fastapi

from src.users.router import user_router


app = fastapi.FastAPI(title="LifeCour$e")


app.include_router(user_router)
