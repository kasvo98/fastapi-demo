from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from dataclasses import dataclass


class Base(DeclarativeBase):
    pass


@dataclass
class Address:
    city: str
    street: str


class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    capacity: Mapped[int]
    city: Mapped[str]
    street: Mapped[str]
    comment: Mapped[str | None]
    floor: Mapped[int]
    has_projector: Mapped[bool]
    internal_note: Mapped[str | None]

    bookings: Mapped[list["Booking"]] = relationship(back_populates="room")

    @property
    def address(self) -> Address:
        return Address(city=self.city, street=self.street)


class Booking(Base):
    __tablename__ = "booking"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))

    room: Mapped["Room"] = relationship(back_populates="bookings")