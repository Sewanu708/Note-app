
from fastapi import APIRouter, status, HTTPException, Depends
from .. import schema
from ..database import get_db
from ..models import User
from .. import utils
from ..oauth2 import create_jwt_token, get_user_details
from sqlalchemy.orm import Session
router = APIRouter(tags=['users'], )

@router.post('/auth/register', status_code=status.HTTP_201_CREATED)
def create_user(payload:schema.User, db:Session =Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
  
    if user :
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
  
    hashed_password = utils.get_password_hashed(payload.password)
    payload.password = hashed_password
    
    print(payload, 'this is payload')
    
    new_user = User(**payload.model_dump())
    
    db.add(new_user)
    db.commit()
    
    db.refresh(new_user)
    
    token = create_jwt_token({"id":new_user.id})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": new_user.id, "email": new_user.email}
    }
    
    
@router.post('/auth/login', status_code=status.HTTP_200_OK)
def login_user(payload:schema.Login, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
  
    if not user  :
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    is_valid =  utils.verify_password(payload.password, user.password)
    
    
    if not is_valid  :
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    
    token = create_jwt_token({"id":user.id})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email}

    }


@router.get('/auth/me', status_code = status.HTTP_200_OK, response_model=schema.UserResponse)
def get_user_details(db:Session =Depends(get_db), id:str = Depends(get_user_details)):

    user = db.query(User).filter(User.id ==id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exists"
        )
    
    return user