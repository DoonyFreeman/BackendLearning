from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import HotelNotFoundHTTPException, \
    RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService
router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples=["2026-04-01"], description="Дата заселения"),
    date_to: date = Query(examples=["2026-05-05"], description="Дата выселения"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "example1": {
                "summary": "Пример 1",
                "value": {
                    "title": "Комната 1",
                    "description": "Очень крутая комната с огромной крутой кроватью",
                    "price": "10000",
                    "quantity": "1",
                    "facilities_ids": [],
                },
            },
            "example2": {
                "summary": "Пример 2",
                "value": {
                    "title": "Luxe",
                    "description": "бизнес люкс с еще большей кроватью",
                    "price": "90000",
                    "quantity": "2",
                    "facilities_ids": [],
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "room": room}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException



@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных о комнате",
    description="Тут мы полностью обновляем данные о комнате",
)
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="Тут мы частично обновляем данные о номере: можно отправить name, а можно title, а можно ничего",
)
async def patch_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep,
):
    await RoomService(db).patch_room(hotel_id, room_id, room_data)
    return {"status": "ok"}

@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление отеля",
    description="Тут мы удаляем отель по его id",
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "ok"}