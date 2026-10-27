from pydantic import BaseModel, Field, model_validator, ConfigDict


class Address(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str
    street: str


class RoomIn(BaseModel):
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

    
class RoomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    capacity: int
    address: Address
    comment: str | None = None
    floor: int
    has_projector: bool