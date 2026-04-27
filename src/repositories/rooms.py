from src.repositories.base import BaseRepository
from src.models import RoomsOrm
from src.schemas.rooms import Room
from datetime import date
from sqlalchemy import select, func
from src.models import BookingsOrm
from src.database import engine

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    def get_filtered_by_time(
            self, 
            hotel_id: int,
            date_from: date,
            date_to: date
    ):  
        rooms_count = ( 
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from >= date_from,
                BookingsOrm.date_to <= date_to
            ).group_by(BookingsOrm.room_id)
            .cte("rooms_count")
        )



        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"), 
                RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte("rooms_left_table")
        )


        query = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0)
        )
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))