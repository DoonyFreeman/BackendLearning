from fastapi import Query, Body, APIRouter, HTTPException
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from datetime import date
from fastapi_cache.decorator import cache
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException
from src.services.hotels import HotelService
from src.exceptions import HotelNotFoundHTTPException


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение списка отелей",
    description="Получение списка отелей с возможностью фильтрации по id и названию",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,  # прокидываем в зависимости от PaginationParams для получения параметров пагинации
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2026-06-01"),
    date_to: date = Query(example="2026-07-02"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )





@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
        


@router.post(
    "",
    summary="Создание отеля",
    description="Создание отеля. id генерируется автоматически, его не нужно передавать в теле запроса",
)
async def create_hotel(
    db: DBDep,
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
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "hotel": hotel}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Тут мы полностью обновляем данные об отеле",
)
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK",}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно отправить name, а можно title, а можно ничего",
)
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
    db: DBDep,
):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "ok"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Тут мы удаляем отель по его id",
)
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "ok"}
