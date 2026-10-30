from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from datetime import datetime, timezone


class BookingIn(BaseModel):
    starts_at: datetime
    ends_at: datetime

    @field_validator("starts_at", "ends_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("Time zone required")
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def check_interval(self) -> "BookingIn":
        if self.ends_at <= self.starts_at:
            raise ValueError("The end time must be later than the start time")
        return self

    
class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    starts_at: datetime
    ends_at: datetime
    room_id: int

    @field_validator("starts_at", "ends_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        return value.replace(tzinfo=timezone.utc)