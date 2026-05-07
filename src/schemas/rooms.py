from pydantic import BaseModel
from pydantic import ConfigDict

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    title: str
    hotel_id: int
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
