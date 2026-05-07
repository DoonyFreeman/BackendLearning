from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100)) # mapped_column нужен для указания типа данных и других параметров столбца в базе данных
    location: Mapped[str] 