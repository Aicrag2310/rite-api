from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import auth as schemas
from app.process import auth as crud
from app.database import get_db

router = APIRouter()

@router.post("/api/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = crud.get_user_by_email(db, email=user.email)
    db_user_phone = crud.get_user_by_phone(db, phone=user.phone)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_phone:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_user(db=db, user=user)
