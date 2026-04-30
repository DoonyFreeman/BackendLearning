from src.repositories.base import BaseRepository
from src.models import BookingsOrm
from src.schemas.bookings import Booking
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper