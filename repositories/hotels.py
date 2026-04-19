from sqlalchemy import select, func
from repositories.base import BaseRepository
from src.models import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
        self,
        location: str | None = None,
        title: str | None = None,
        limit: int | None = None,
        offset: int | None = None
    ):
        query = select(HotelsOrm)
        if location: 
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title: 
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)



        return result.scalars().all()
