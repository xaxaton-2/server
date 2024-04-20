# Red Hot OSU Peppers
### BACKEND
___
## Локальный запуск проекта
__1. Клонируйте репозиторий__
```
git clone https://github.com/xaxaton-2/server.git
```
__2. Установите Poetry и зависимости проекта__
```
pip install poetry databases aiosqlite

poetry install
```
__3. Установите миграции alembic__
```
alembic revision --autogenerate -m "Create DB"

alembic upgrade head
```
__4. Задать секреты__
Создать .env в корне с следующим наполнением:
```
SECRET_KEY = example
```

__5. Запустить проект__
```
uvicorn src.main:app --reload
```