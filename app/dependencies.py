from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Room


def get_pagination(skip: int = 0, limit: int = 10) -> dict:
    return {"skip": skip, "limit": limit}


def get_room_or_404(room_id: int, db: Session = Depends(get_db)) -> Room:
    room = db.get(Room, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room