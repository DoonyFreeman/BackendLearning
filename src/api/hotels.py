from fastapi import Query, Body, APIRouter
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from datetime import date

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение списка отелей",
    description="Получение списка отелей с возможностью фильтрации по id и названию",
)
async def get_hotels(
    pagination: PaginationDep,  # прокидываем в зависимости от PaginationParams для получения параметров пагинации
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date | None = Query(example="2026-06-01", description="Дата заселения"),
    date_to: date | None = Query(example="2026-07-02", description="Дата выселения"),
):
   per_page = pagination.per_page or 5
   return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
    )
#    return await db.hotels.get_all(
#        location = location,
#        title = title,
#        limit=per_page,
#        offset=per_page * (pagination.page - 1) if pagination.page and pagination.per_page else 0
#     )



@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "hotel": hotel}

@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Тут мы полностью обновляем данные об отеле",
)
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    hotel = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK", "hotel": hotel}



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
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Тут мы удаляем отель по его id",
)
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ok"}

