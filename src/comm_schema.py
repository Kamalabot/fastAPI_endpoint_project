from pydantic import BaseModel, EmailStr
from datetime import datetime

class req_post(BaseModel):
    title:str
    content:str
    is_published: bool = True

class create_post(req_post):
    pass

class res_post(BaseModel):
    title:str
    is_published:bool
    post_id:int
    time_created:datetime
    #created_at: datetime
#the below class is declared to help pydantic model to convert the 
#sqlalchemy object to dict
    class Config:
        orm_mode = True

class create_user(BaseModel):
    email:EmailStr
    password:str

class res_user(BaseModel):
    user_id:str
    email:EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str
