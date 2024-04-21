import jwt

import fastapi

from src.users import crud
from src import settings


def generate_jwt_token(pk):
    token = jwt.encode(
        {"id": pk},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return token


async def authenticate(token):
    return await authenticate_credentials(token)


async def authenticate_credentials(token):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
    except Exception:
        raise fastapi.HTTPException(
            status_code=403,
            detail="Ошибка аутентификации. Невозможно декодировать токен"
        )

    user = await crud.get_user_by_id(payload["id"])
    if not user:
        raise fastapi.HTTPException(
            status_code=403,
            detail="Пользователь не найден"
        )

    return (user, token)
