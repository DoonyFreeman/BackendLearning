from typing import Sequence

from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model: RoomsFacilitiesOrm = RoomsFacilitiesOrm  # type: ignore
    mapper = RoomFacilityDataMapper

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        get_current_facilities_ids_query = select(self.model.facility_id).filter_by(room_id=room_id)  # type: ignore
        # Ищем различия между новыми и старыми значениями
        res = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids: Sequence[int] = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = delete(self.model).filter(  # type: ignore
                self.model.room_id == room_id, self.model.facility_id.in_(ids_to_delete)  # type: ignore
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stmt = insert(self.model).values(  # type: ignore
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert]
            )
            await self.session.execute(insert_m2m_facilities_stmt)
