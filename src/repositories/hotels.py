from sqlalchemy import select, func
from src.repositories.base import BaseRepository
from src.models import HotelsOrm
from src.schemas.hotels import Hotel
from datetime import date
from src.models import RoomsOrm, BookingsOrm
from src.database import engine


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location: str | None = None,
            title: str | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[Hotel]:
        rooms_count = ( 
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from
            ).group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )


        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"), 
                RoomsOrm.hotel_id.label("hotel_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )
        
        available_hotels = (
            select(rooms_left_table.c.hotel_id)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0)
            .group_by(rooms_left_table.c.hotel_id)
            .cte(name="available_hotels")
        )
        
        query = (
            select(HotelsOrm)
            .filter(HotelsOrm.id.in_(select(available_hotels.c.hotel_id)))
        )
        
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        
        query = query.limit(limit).offset(offset)
        
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]