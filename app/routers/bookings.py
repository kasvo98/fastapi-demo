from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..schemas.bookings import BookingOut
from ..models import Room, Booking
from ..dependencies import get_db, get_room_or_404


router = APIRouter()


@router.post("/{room_id}/bookings", status_code=status.HTTP_201_CREATED, response_model=BookingOut)
def create_booking(room: Room = Depends(get_room_or_404), db: Session = Depends(get_db)):
    booking = Booking(room_id=room.id)
    db.add(booking)
    db.commit()
    return booking


@router.get("/{room_id}/bookings", response_model=list[BookingOut])
def list_bookings(room: Room = Depends(get_room_or_404), db: Session = Depends(get_db)):
    return db.scalars(select(Booking).where(Booking.room_id == room.id)).all()