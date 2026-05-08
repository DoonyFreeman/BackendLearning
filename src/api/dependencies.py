from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel
from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Номер страницы", ge=1)]
    per_page: Annotated[
        int | None, Query(None, description="Количество отелей на странице", ge=1, lt=30)
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    user_id = data.get("user_id")
    if not isinstance(user_id, int):
        raise HTTPException(status_code=401, detail="Неверный токен")
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
