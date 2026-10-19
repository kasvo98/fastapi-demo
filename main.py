from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field, model_validator


app = FastAPI()

rooms_db : dict[int, dict] = {}
next_id = 1

class Address(BaseModel):
    city: str
    street: str

class RoomIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    capacity: int = Field(..., ge=1, le=50)
    address: Address
    comment: str | None = None
    floor: int = 0
    has_projector: bool = False

class RoomOut(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=50)
    capacity: int = Field(..., ge=1, le=50)
    address: Address
    comment: str | None = None
    floor: int = 0
    has_projector: bool = False

class RoomPatch(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    capacity: int | None = Field(None, ge=1, le=50)
    address: Address | None = None
    comment: str | None = None
    floor: int | None = None
    has_projector: bool | None = None

    _non_nullable_fields = {"name", "capacity", "address", "floor", "has_projector"}

    @model_validator(mode="after")
    def check_invalid_nulls(self):
        invalid_nulls = [field for field in self._non_nullable_fields 
                         if field in self.model_fields_set and getattr(self, field) is None]
        if invalid_nulls:
            raise ValueError(f"Null is not allowed for fields: {", ".join(invalid_nulls)}")
        return self


def get_room_or_404(room_id: int) -> dict:
    room = rooms_db.get(room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room


@app.get("/api/rooms")
def list_rooms(min_capacity: int = 0, has_projector: bool | None = None):
    result = [r for r in rooms_db.values() if r["capacity"] >= min_capacity]
    if has_projector is not None:
        result = [r for r in result if r["has_projector"] == has_projector]
    return result


@app.post("/api/rooms", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomIn):
    global next_id
    current_id = next_id
    rooms_db[current_id] = {"id": current_id, **room.model_dump()}
    next_id += 1
    return {**rooms_db[current_id], "internal_note": "my_note"}


@app.get("/api/rooms/{room_id}", response_model=RoomOut)
def read_room(room_id: int):
    return get_room_or_404(room_id)


@app.put("/api/rooms/{room_id}", response_model=RoomOut)
def update_room(room_id: int, room: RoomIn):
    existing = get_room_or_404(room_id)
    rooms_db[room_id] = {"id": room_id, **room.model_dump()}
    return rooms_db[room_id]


@app.patch("/api/rooms/{room_id}", response_model=RoomOut)
def patch_room(room_id: int, room: RoomPatch):
    existing = get_room_or_404(room_id)

    for field in room.model_fields_set:
        existing[field] = getattr(room, field)
        
    return existing
