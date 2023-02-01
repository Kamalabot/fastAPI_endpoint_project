#we implement the authentication process here
from fastapi import Depends, FastAPI,Response,status,HTTPException, APIRouter
from fastapi.params import Body

from .. import models 
from ..utils import hasher, verify_pass
from ..comm_schema import UserLogin 
from typing import List

#The ORM engine is created in separate file called database
from sqlalchemy.orm import Session
from ..databaseORM import get_db

router = APIRouter(tags=['Auth'])

@router.post('/login')
def login(user_cred:UserLogin,db : Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.email == user_cred.email).first()
    
    if not user_data:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the user_id is not found"))

    verification = verify_pass(user_cred.password, user_data.password) 
    
    if not verification:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Wrong Password"))
    return {"token":"example"}


    
      


