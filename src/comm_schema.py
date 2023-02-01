from pydantic import BaseModel
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
    #created_at: datetime
#the below class is declared to help pydantic model to convert the 
#sqlalchemy object to dict
    class Config:
        orm_mode = True
