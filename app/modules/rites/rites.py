from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import rites as schemas
from app.process import rites as crud_rite
from app.process import vehicle as crud_vehicle
from app.orm import User
from app.database import get_db
from app.deps import get_current_driver_user
from app.orm import RiteStatus

router = APIRouter()

@router.post("/api/rites", response_model=schemas.Rite, status_code=status.HTTP_201_CREATED)
def create_new_rite(
    rite: schemas.RiteCreate,
    db: Session = Depends(get_db),
    #current_user: User = Depends(get_current_driver_user)
):
    """
    Crea un nuevo rite para el conductor autenticado.

    - **vehicle_id**: El ID del vehículo que se usará para el viaje.
    - **origin**: Punto de partida.
    - **destination**: Punto de llegada.
    - **departure_time**: Fecha y hora de salida (formato ISO 8601: "2025-12-31T23:59:59").
    - **price_per_seat**: Costo por asiento.
    - **available_seats**: Número de asientos disponibles para pasajeros.
    - **description**: (Opcional) Descripción del viaje.
    - **instructions**: (Opcional) Instrucciones para el punto de encuentro.
    """
    # Verificación de seguridad: Asegurarse de que el vehículo pertenece al conductor.
    vehicle = crud_vehicle.get_vehicle_by_id(db, vehicle_id=rite.vehicle_id)
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Vehicle not found"
        )
    if vehicle.driver_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create a rite with your own vehicle"
        )
    
    return crud_rite.create_rite(db=db, rite=rite, driver_id=1)


@router.get("/api/rites", response_model=List[schemas.Rite])
def read_driver_rites(
    status: Optional[RiteStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    #current_user: User = Depends(get_current_driver_user)
):
    """
    Obtiene los rites del conductor autenticado.
    Se puede filtrar por estado: 'upcoming', 'in-progress', 'completed', 'cancelled'.
    """
    rites = crud_rite.get_rites_by_driver(
        db=db, driver_id=1, status=status, skip=skip, limit=limit
    )
    return rites
