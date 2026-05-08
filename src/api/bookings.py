from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.rooms import Room
from src.schemas.hotels import Hotel

from src.exceptions import ObjectNotFoundException

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me")
async def get_user_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    
    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)  # type: ignore
    
    room_price: int = room.price  # type: ignore
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)  # type: ignore
    await db.commit()
    return {"status": "OK", "data": booking}
