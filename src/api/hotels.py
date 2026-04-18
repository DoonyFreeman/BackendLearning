from fastapi import Query, Body, APIRouter
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from typing import Annotated
from src.database import async_session_maker, engine
from src.models import HotelsOrm
from sqlalchemy import insert, select


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение списка отелей",
    description="Получение списка отелей с возможностью фильтрации по id и названию",
)
async def get_hotels(
    pagination: PaginationDep,  # прокидываем в зависимости от PaginationParams для получения параметров пагинации
    id: int | None = Query(None, description="id отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
   

   async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)
        print(type(result), result)
        hotels = result.scalars().all()
        return hotels
    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page - 1) :][
    #         : pagination.per_page
    #     ]
    # else:


@router.post(
    "",
    summary="Создание отеля",
    description="Создание отеля. id генерируется автоматически, его не нужно передавать в теле запроса",
)
async def create_hotel(
    hotel_data: Hotel = Body(
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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"Status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Тут мы полностью обновляем данные об отеле",
)
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK", "hotel": hotel}
    return {"status": "error", "message": "Hotel not found"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно отправить name, а можно title, а можно ничего",
)
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "ok", "hotel": hotel}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Тут мы удаляем отель по его id",
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"Status": "OK"}
