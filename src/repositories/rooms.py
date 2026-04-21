from src.repositories.base import BaseRepository
from src.models import RoomsOrm
from src.schemas.users import User



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = User