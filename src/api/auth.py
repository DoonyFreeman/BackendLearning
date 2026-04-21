from fastapi import APIRouter
from src.shchemas.users import UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация аутентификация"])

@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    
    hashed_password = "dfwef78"
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}