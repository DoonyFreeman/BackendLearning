from src.database import async_session_maker_null_pool
from src.schemas.bookings import BookingAdd
from src.utils.db_manager import DBManager
from datetime import date

async def test_add_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=1000,
    )
    await db.bookings.add(booking_data)
    await db.commit()
