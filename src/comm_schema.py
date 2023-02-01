from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

class req_post(BaseModel):
    title:str
    content:str
    is_published: bool = True

class create_post(req_post):
    pass

class res_user(BaseModel):
    user_id:str
    email:EmailStr

    class Config:
        orm_mode = True


class res_post(BaseModel):
    title:str
    is_published:bool
    post_id:int
    owner_id:int
    time_created:datetime
    owner : res_user
    #created_at: datetime
#the below class is declared to help pydantic model to convert the 
#sqlalchemy object to dict
    class Config:
        orm_mode = True

class create_user(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_typ: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)
