from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Booking


def to_db_utc(value: datetime) -> datetime:
    if value.utcoffset() is None:
        raise ValueError("Требуется часовой пояс")
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def find_conflict(
    db: Session,
    room_id: int,
    new_start: datetime,
    new_end: datetime,
) -> Booking | None:
    start_utc = to_db_utc(new_start)
    end_utc = to_db_utc(new_end)
    statement = select(Booking).where(
        Booking.room_id == room_id,
        Booking.starts_at < end_utc,
        Booking.ends_at > start_utc,
    )
    return db.scalars(statement).first()