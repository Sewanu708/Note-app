from fastapi import HTTPException, status, Depends
from datetime import datetime, timedelta, timezone
from jose import jwt
from .config import settings
from .database import get_db
from sqlalchemy.orm import Session
from .models import User

from fastapi.security import OAuth2PasswordBearer

SECRET_KEY  = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.expiry_time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
        
def create_jwt_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token:str):
    try:
        print(token )
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(decoded_data)
        id = decoded_data.get('id')
        
        if id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid JSON Web Token')

        return id
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid JSON Web Token')
 
 

def get_user_details(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    if not token:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    user_id = verify_jwt_token(token)
    user_data = db.query(User).filter(User.id == user_id).first()
    
    if user_data is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    return user_data.id