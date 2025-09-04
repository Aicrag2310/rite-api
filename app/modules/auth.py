from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Header, Depends
from datetime import datetime
from app.models import auth as schemas
from app.database import get_db
from app import get_settings
from app.orm import User
from app.models import AppGenericException
from jose.constants import ALGORITHMS
import uuid
from jose import jwt
from passlib.context import CryptContext

router = APIRouter()


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=15000,
)


@router.post('/token', tags=['auth'])
def auth(request_data: schemas.AuthRequest,
         accept_language: str = Header(default='en'),
         db: Session = Depends(get_db)):
    
    config = get_settings()

    username = request_data.username
    password = request_data.password

    print ('Que es ', username)
    user = db.query(User).filter_by(email=username).first()
    print ('Voy aqui')
    if not user:
        print ('Holaaa')
        raise AppGenericException(0, 'Usuario no encontrado.', 404)
    print ('Usuario existe')
    if int(user.active) != 1:
        raise AppGenericException(1, 'Usuario inhabilitado.', 403)
    print ('Usuario encontrado ', user.email)
    if not pwd_context.verify(password, user.hashed_password):
        raise AppGenericException(2, 'Contraseña invalida', 400)
    print ('Usuario valido')
    now_seconds = int(datetime.now().timestamp())
    token = jwt.encode({
            'iat': now_seconds,
            'nbf': now_seconds,
            'jti': str(uuid.uuid4()),
            'identity': user.id,
            'fresh': False,
            'type': 'access',
        }, config.secret, algorithm=ALGORITHMS.HS256)
    print ('Token ', token )
    return {'token': token}