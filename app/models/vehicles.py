from pydantic import BaseModel, EmailStr
from typing import Optional
from app.orm import UserRole

class VehicleBase(BaseModel):
    brand: str
    model: str
    plate: str
    color: str
    seats: int

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    brand: Optional[str] = None
    model: Optional[str] = None
    plate: Optional[str] = None
    color: Optional[str] = None
    seats: Optional[int] = None

class Vehicle(VehicleBase):
    id: int
    driver_id: int

    class Config:
        orm_mode = True