
from fastapi import Depends, FastAPI,Response,status,HTTPException, APIRouter
from fastapi.params import Body
import time

from .. import models 
from ..utils import hasher
from ..comm_schema import res_user, create_user
from typing import List

#The ORM engine is created in separate file called database
from sqlalchemy.orm import Session
from ..databaseORM import get_db

router = APIRouter()

@router.post("/addusers",status_code=status.HTTP_201_CREATED,response_model=res_user)
def add_users(user_load:create_user,db: Session = Depends(get_db)):
    #hash the password
    #pass_hash = passwd_context.hash(user_load.password)
    #update the hashed password into the dict
    user_load.password = hasher(user_load.password)
    new_user = models.User(**user_load.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/get_users",response_model=List[res_user])
def get_users(db: Session = Depends(get_db)):
    #querying the database session
    data_users = db.query(models.User).all()
    return data_users

@router.get('/get_id/{user_id}',response_model = res_user)
def find_user(user_id:int, db: Session = Depends(get_db)):
    one_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if one_user == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the id is not found"))
    return one_user


