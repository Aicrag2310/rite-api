
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.orm import RiteStatus

class RiteBase(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    price_per_seat: float
    available_seats: int
    description: Optional[str] = None
    instructions: Optional[str] = None
    vehicle_id: int

class RiteCreate(RiteBase):
    pass

class Rite(RiteBase):
    id: int
    driver_id: int
    status: RiteStatus

    class Config:
        orm_mode = True
