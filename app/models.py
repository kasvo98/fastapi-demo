from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
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

    @property
    def address(self) -> Address:
        return Address(city=self.city, street=self.street)