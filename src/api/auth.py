from fastapi import APIRouter, HTTPException, Response
import jwt
from datetime import datetime, timedelta, timezone



from src.schemas.users import UserRequestAdd, UserAdd

from src.config import settings
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep
from src.api.dependencies import DBDep
router = APIRouter(prefix="/auth", tags=["Авторизация аутентификация"])





def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt




@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep

):  
    try:
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await db.users.add(new_user_data)
        await db.commit()
    except:
         raise HTTPException(status_code=400)
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep
):
    


        user = await db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не найден")
        
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token}
    


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.get("/logout")
async def logout(
    response: Response
):
    response.delete_cookie("access_token")
    return {"status": "OK"}