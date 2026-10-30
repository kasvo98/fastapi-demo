from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..schemas.bookings import BookingIn, BookingOut
from ..models import Room, Booking
from ..dependencies import get_db, get_room_or_404
from ..booking_utils import to_db_utc, find_conflict


router = APIRouter()


@router.post("/{room_id}/bookings", status_code=status.HTTP_201_CREATED, response_model=BookingOut)
def create_booking(data: BookingIn, room: Room = Depends(get_room_or_404), db: Session = Depends(get_db)):
    if find_conflict(db, room.id, data.starts_at, data.ends_at):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Booking conflict")
    booking = Booking(
        room_id=room.id,
        starts_at=to_db_utc(data.starts_at),
        ends_at=to_db_utc(data.ends_at))
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/{room_id}/bookings", response_model=list[BookingOut])
def list_bookings(room: Room = Depends(get_room_or_404), db: Session = Depends(get_db)):
    return db.scalars(select(Booking).where(Booking.room_id == room.id)).all()