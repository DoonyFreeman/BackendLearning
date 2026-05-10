from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    UserAlreadyExistsException,
    EmailNotRegisteredException,
    IncorrectPasswordException,
    UserEmailAlreadyExistsHTTPException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordHTTPException,

)
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep,
):
    try:
        user = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    user = await AuthService(db).get_one_or_none_user(user_id)
    return user


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
