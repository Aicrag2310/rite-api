from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import vehicles as schemas
from app.process import vehicle as crud_vehicle
from app.orm import User
from app.database import get_db
from app.deps import get_current_driver_user

router = APIRouter()

@router.post("/", response_model=schemas.Vehicle, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle: schemas.VehicleCreate,
    db: Session = Depends(get_db),
    #current_user: User = Depends(get_current_driver_user)
):
    db_vehicle = crud_vehicle.get_vehicle_by_plate(db, plate=vehicle.plate)
    if db_vehicle:
        raise HTTPException(status_code=400, detail="Plate already registered")
    return crud_vehicle.create_driver_vehicle(db=db, vehicle=vehicle, driver_id=1)

@router.get("/", response_model=List[schemas.Vehicle])
def read_vehicles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    #current_user: User = Depends(get_current_driver_user)
):
    """
    Obtiene la lista de vehículos del conductor autenticado.
    """
    vehicles = crud_vehicle.get_vehicles_by_driver(db, driver_id=1, skip=skip, limit=limit)
    return vehicles
