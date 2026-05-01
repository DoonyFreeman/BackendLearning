from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd



router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
@cache(expire=60)
async def get_facilities(db: DBDep):
    print("Иду в базу данных")
    return await db.facilities.get_all()




@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "room": facility}



