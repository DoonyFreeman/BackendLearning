from fastapi import Query, Body, APIRouter
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep
from typing import Annotated
from src.database import async_session_maker, engine
from src.models import HotelsOrm
from sqlalchemy import insert, select, func
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение списка отелей",
    description="Получение списка отелей с возможностью фильтрации по id и названию",
)
async def get_hotels(
    pagination: PaginationDep,  # прокидываем в зависимости от PaginationParams для получения параметров пагинации
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
):
   per_page = pagination.per_page or 5
   async with async_session_maker() as session:
       return await HotelsRepository(session).get_all(
           location = location,
            title = title,
            limit=per_page,
            offset=per_page * (pagination.page - 1) if pagination.page and pagination.per_page else 0
       )



@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post(
    "",
    summary="Создание отеля",
    description="Создание отеля. id генерируется автоматически, его не нужно передавать в теле запроса",
)
async def create_hotel(
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "example1": {
                "summary": "Пример 1",
                "value": {
                    "title": "Sochi",
                    "location": "Ул Ленина, 1",
                },
            },
            "example2": {
                "summary": "Пример 2",
                "value": {
                    "title": "Krim",
                    "location": "Ул Ленина, 2",
                },
            },
        },
    ),
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "hotel": hotel}

@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Тут мы полностью обновляем данные об отеле",
)
async def put_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()



@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно отправить name, а можно title, а можно ничего",
)
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "ok"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Тут мы удаляем отель по его id",
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "ok"}
