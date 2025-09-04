from sqlalchemy.orm import Session
from app.models import vehicles as schemas
from app.orm import Vehicle

def get_vehicle_by_plate(db: Session, plate: str):
    return db.query(Vehicle).filter(Vehicle.plate == plate).first()

def get_vehicles_by_driver(db: Session, driver_id: int, skip: int = 0, limit: int = 100):
    return db.query(Vehicle).filter(Vehicle.driver_id == driver_id).offset(skip).limit(limit).all()

def create_driver_vehicle(db: Session, vehicle: schemas.VehicleCreate, driver_id: int):
    db_vehicle = Vehicle(**vehicle.dict(), driver_id=driver_id)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle
# --- AÑADIR ESTA FUNCIÓN ---
def get_vehicle_by_id(db: Session, vehicle_id: int):
    """
    Obtiene un vehículo por su ID.
    """
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()