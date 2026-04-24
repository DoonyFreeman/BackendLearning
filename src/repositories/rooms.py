from src.repositories.base import BaseRepository
from src.models import RoomsOrm
from src.schemas.rooms import Room



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room