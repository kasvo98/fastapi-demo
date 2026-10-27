from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..schemas.rooms import RoomIn, RoomOut, RoomPatch
from ..models import Room
from ..database import get_db
from ..dependencies import get_pagination, get_room_or_404


router = APIRouter()


@router.get("/{room_id}", response_model=RoomOut)
def get_room(room: int = Depends(get_room_or_404)):
    return room


@router.get("", response_model=list[RoomOut])
def list_rooms(min_capacity: int = 0, has_projector: bool | None = None, pagination: dict = Depends(get_pagination),
               db: Session = Depends(get_db)):
    statement = select(Room).where(Room.capacity >= min_capacity)
    if has_projector is not None:
        statement = statement.where(Room.has_projector == has_projector)
    result = db.scalars(statement).all()
    result = result[pagination["skip"] : pagination["skip"] + pagination["limit"]]
    return result


@router.post("", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
def create_room(data: RoomIn, db: Session = Depends(get_db)):
    room = Room(
        **data.model_dump(exclude={"address"}),
        **data.address.model_dump(),
        internal_note="internal note")
    db.add(room)
    db.commit()
    return room


@router.put("/{room_id}", response_model=RoomOut)
def update_room(data: RoomIn, room: Room = Depends(get_room_or_404), db: Session = Depends(get_db)):
    data_flat = {**data.model_dump(exclude={"address"}), **data.address.model_dump()}
    for field, value in data_flat.items():
        setattr(room, field, value)
    db.commit()
    return room


@router.patch("/{room_id}", response_model=RoomOut)
def patch_room(data: RoomPatch, room: Room = Depends(get_room_or_404), db: Session = Depends(get_db)):
    for field in data.model_fields_set:
        if field == "address" and data.address is not None:
            room.city = data.address.city
            room.street = data.address.street
        else:
            setattr(room, field, getattr(data, field))        
    db.commit()
    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room: Room = Depends(get_room_or_404), db: Session = Depends(get_db)):
    if room.bookings:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Room has bookings")
    db.delete(room)
    db.commit()
