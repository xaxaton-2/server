import fastapi

from src.auth.router import router


app = fastapi.FastAPI(title="LifeCour$e")


app.include_router(router)
