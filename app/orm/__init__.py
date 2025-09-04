from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date, Table, func, Text
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
import enum


class UserRole(str, enum.Enum):
    passenger = "passenger"
    driver = "driver"


class RiteStatus(str, enum.Enum):
    upcoming = "upcoming"
    in_progress = "in-progress"
    completed = "completed"
    cancelled = "cancelled"

class Rite(Base):
    __tablename__ = "rites"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    price_per_seat = Column(Float, nullable=False)
    available_seats = Column(Integer, nullable=False)
    status = Column(SQLAlchemyEnum(RiteStatus), nullable=False, default=RiteStatus.upcoming)
    description = Column(String(500), nullable=True)
    instructions = Column(String(500), nullable=True)

    driver_id = Column(Integer, ForeignKey("users.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    driver = relationship("User", back_populates="rites_driven")
    vehicle = relationship("Vehicle", back_populates="rites")

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    plate = Column(String(15), unique=True, index=True, nullable=False)
    color = Column(String(30), nullable=False)
    seats = Column(Integer, nullable=False)

    # Clave foránea para vincular con el usuario (conductor)
    driver_id = Column(Integer, ForeignKey("users.id"))
    
    # Relación inversa para poder acceder al conductor desde un vehículo como vehicle.driver
    driver = relationship("User", back_populates="vehicles")
    rites = relationship("Rite", back_populates="vehicle")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Integer, default=1)

    vehicles = relationship("Vehicle", back_populates="driver")
    rites_driven = relationship("Rite", back_populates="driver")


tables_shortnames = {
}
