from fastapi import APIRouter, Body, Query, HTTPException
from datetime import date


from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.schemas.facilities import RoomFacilityAdd
from src.api.dependencies import DBDep  # noqa: F401
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, RoomNotFoundHTTPException, HotelNotFoundHTTPException

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples=["2026-04-01"], description="Дата заселения"),
    date_to: date = Query(examples=["2026-05-05"], description="Дата выселения"),
):
    check_date_to_after_date_from(date_from=date_from, date_to=date_to)
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


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
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids  # type: ignore
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "room": room}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)    
    if not room:
        raise RoomNotFoundHTTPException()
    return room


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных о комнате",
    description="Тут мы полностью обновляем данные о комнате",
)
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException()
    
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
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
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException()
    
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление отеля",
    description="Тут мы удаляем отель по его id",
)
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException()
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}
