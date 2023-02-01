#we implement the authentication process here
from fastapi import Depends, FastAPI,Response,status,HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Body

from .. import models 
from ..utils import hasher, verify_pass
from ..comm_schema import UserLogin 
from typing import List

#The ORM engine is created in separate file called database
from sqlalchemy.orm import Session
from ..databaseORM import get_db

#importing the jwt oauth module

from ..oauth import create_access_token

router = APIRouter(tags=['Auth'])

@router.post('/login')
def login(user_cred:OAuth2PasswordRequestForm = Depends(),
          db : Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.email == user_cred.username).first()
    
    if not user_data:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the user_id is not found"))

    verification = verify_pass(user_cred.password, user_data.password) 
    
    if not verification:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Wrong Password"))

    access_token = create_access_token(data = {"user_id":user_cred.username})
    return {"access_token":access_token, "token_type":"bearer"}


    
      


