"""
Seed script to populate database with test data for 2026 year
"""
import asyncio
from datetime import date

from src.database import async_session_maker, engine, Base
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm
from src.models.users import UsersOrm
from sqlalchemy import insert


async def seed_data():
    async with async_session_maker() as session:
        user = insert(UsersOrm).returning(UsersOrm.id).values(
            email="test@test.com",
            hashed_password="$2b$12$hashedpasswordplaceholder"
        )
        result = await session.execute(user)
        user_id = result.scalar_one()
        print(f"Created user (id={user_id})")
        
        hotels = [
            {"title": "Sochi Resort", "location": "Сочи, Морской переулок 5"},
            {"title": "Moscow Grand", "location": "Москва, улица Ленина 10"},
            {"title": "Kazan Palas", "location": "Казань, улица Баумана 25"},
            {"title": "Peterhof Gold", "location": "Петергоф, Санкт-Петербургское шоссе 30"},
        ]
        
        hotel_ids = []
        for hotel in hotels:
            stmt = insert(HotelsOrm).returning(HotelsOrm.id).values(**hotel)
            result = await session.execute(stmt)
            hotel_id = result.scalar_one()
            hotel_ids.append(hotel_id)
            print(f"Created hotel: {hotel['title']} (id={hotel_id})")
        
        await session.commit()
        
        rooms_data = [
            {"title": "Стандартный номер", "description": "Уютный номер с видом на море", "price": 5000, "quantity": 2},
            {"title": "Люкс с балконом", "description": "Просторный люкс с балконом", "price": 12000, "quantity": 1},
            {"title": "Семейный номер", "description": "Большая комната для семьи", "price": 8000, "quantity": 3},
            {"title": "Бизнес номер", "description": "Для деловых поездок", "price": 7000, "quantity": 5},
            {"title": "Премьер", "description": "Номер премиум класса", "price": 15000, "quantity": 2},
            {"title": "Исторический", "description": "Номер в классическом стиле", "price": 6000, "quantity": 4},
            {"title": "Королевский люкс", "description": "Люкс с видом на фонтаны", "price": 20000, "quantity": 1},
        ]
        
        room_ids = []
        for i, room in enumerate(rooms_data):
            room["hotel_id"] = hotel_ids[i // 2]
            stmt = insert(RoomsOrm).returning(RoomsOrm.id).values(**room)
            result = await session.execute(stmt)
            room_id = result.scalar_one()
            room_ids.append(room_id)
            print(f"Created room: {room['title']} (id={room_id})")
        
        await session.commit()
        
        bookings = [
            {"room_id": room_ids[0], "date_from": date(2026, 6, 1), "date_to": date(2026, 6, 5), "price": 5000},
            {"room_id": room_ids[1], "date_from": date(2026, 6, 10), "date_to": date(2026, 6, 15), "price": 12000},
            {"room_id": room_ids[4], "date_from": date(2026, 7, 1), "date_to": date(2026, 7, 5), "price": 7000},
            {"room_id": room_ids[6], "date_from": date(2026, 8, 1), "date_to": date(2026, 8, 10), "price": 20000},
        ]
        
        for booking in bookings:
            stmt = insert(BookingsOrm).returning(BookingsOrm.id).values(user_id=user_id, **booking)
            result = await session.execute(stmt)
            booking_id = result.scalar_one()
            print(f"Created booking #{booking_id} for room {booking['room_id']}")
        
        await session.commit()
    
    print("\n=== Данные созданы! ===")
    print("\nТестируй:")
    print('GET /hotels?date_from=2026-06-01&date_to=2026-06-10')
    print('GET /hotels/1/rooms?date_from=2026-06-01&date_to=2026-06-10')
    print('GET /hotels?date_from=2026-07-01&date_to=2026-07-10')
    print('GET /hotels?date_from=2026-08-01&date_to=2026-08-15')


if __name__ == "__main__":
    asyncio.run(seed_data())