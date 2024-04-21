import fastapi
from fastapi.middleware.cors import CORSMiddleware

from src.users.router import user_router
from src.company.router import company_router


app = fastapi.FastAPI(title="LifeCour$e")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(company_router)
