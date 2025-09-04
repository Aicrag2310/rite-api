from sqlalchemy.orm import Session
from app.models import rites as schemas
from app.orm import Rite, RiteStatus
from typing import Optional


def create_rite(db: Session, rite: schemas.RiteCreate, driver_id: int):
    """
    Crea un nuevo rite en la base de datos.
    """
    db_rite = Rite(
        **rite.dict(),
        driver_id=driver_id,
        status=RiteStatus.upcoming
    )
    db.add(db_rite)
    db.commit()
    db.refresh(db_rite)
    return db_rite



def get_rites_by_driver(db: Session, driver_id: int, status: Optional[RiteStatus] = None, skip: int = 0, limit: int = 100):
    """
    Obtiene los rites de un conductor, opcionalmente filtrados por estado.
    """
    query = db.query(Rite).filter(Rite.driver_id == driver_id)
    if status:
        query = query.filter(Rite.status == status)
    
    # Ordenar por fecha de salida descendente para ver los más recientes primero
    query = query.order_by(Rite.departure_time.desc())

    return query.offset(skip).limit(limit).all()

