import fastapi
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from database import User
from auth.manager import get_user_manager
from auth.schema import UserCreate, UserRead


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

app = fastapi.FastAPI(title="BEBRA")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    tags=['auth'],
    prefix='/auth/jwt'
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)

current_user = fastapi_users.current_user()


@app.get('/protected')
def protected(user: User = fastapi.Depends(current_user)):
    return user
