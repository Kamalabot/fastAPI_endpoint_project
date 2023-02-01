#!/usr/bin/env python

##During the initial dev, the responses for each path was having object signature
## of {'name':data:Dict}. This is useful for knowing what the route is sending 
#back. After the initial dev, the program is cleaned and the additional indicators
#are removed

#This is the mail script where the PG database connectivity is implemented 
# required for return appropriate response when the result is Null

from fastapi import Depends, FastAPI,Response,status,HTTPException
from fastapi.params import Body
import time
from typing import List

#models module contains the real database table schema that 
#established the connectivity to tables that is required in this api 
from . import models

#The ORM engine is created in separate file called database
from sqlalchemy.orm import Session
from .databaseORM import engine, get_db

models.Base.metadata.create_all(bind=engine)

#importing the communication schema from separate file
from .comm_schema import req_post,create_post,res_post,create_user,res_user

from .utils import hasher

app = FastAPI()

#below decorator informs path and http method
@app.get("/")
#async root function is initiated
async def root():
    #When the root function is called the message is 
    #is returned.
    return {"db_server":"This is from Database Server"}

#The other /posts has been deleted 
@app.get("/posts",response_model=List[res_post])
def get_ormres(db: Session = Depends(get_db)):
    #querying the database session
    data_posts = db.query(models.Post).all()
    return data_posts

#lets make createposts useful and load data into local_posts array

@app.post("/addposts",status_code=status.HTTP_201_CREATED,response_model=res_post)
def add_posts(load: req_post,db: Session = Depends(get_db)):

#**load.dict() will take care of converting the variables in the format models will accept
    new_post = models.Post(**load.dict())
    #new_post = models.Post(title=load.title, content=load.content, is_published=load.is_published)
#need to present the query to engine
    db.add(new_post)
#query needs to be comitted
    db.commit()
#After that the refreshed database needs to be stored back in to the variable
    db.refresh(new_post)
    return new_post

'''
@app.get("/params/latest")
def get_recent(db: Session = Depends(get_db)):
    data_posts = db.query(models.Post).order_by('post_id').all()
    return data_posts
'''

@app.get("/params/{prm}")
#Note the :int, this will validate the parameter
def print_params(prm :int, db: Session = Depends(get_db)):
    one_row = db.query(models.Post).filter(models.Post.post_id == prm).first()
    if not one_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The id {prm} is not found')
    return one_row

@app.delete("/delete/{id}",status_code = status.HTTP_204_NO_CONTENT)
#when using the 204 status, the remaining posts or any data cannot be sent
def delete_posts(id :int,db: Session = Depends(get_db)):
    one_row = db.query(models.Post).filter(models.Post.post_id == id) 
    if one_row.first() == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the id is not found"))
    one_row.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/{id}",status_code=status.HTTP_201_CREATED,response_model=res_post)
def update_post(id :int,post:create_post,db: Session = Depends(get_db)):
    save_query = db.query(models.Post).filter(models.Post.post_id == id)

    if save_query.first()== None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND))

    save_query.update(post.dict(),synchronize_session=False)
    db.commit()

    #update the id in the recieved data and replace that in the local_posts
    return save_query.first()

###We will start creating routes for user addition####

@app.post("/addusers",status_code=status.HTTP_201_CREATED,response_model=res_user)
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

@app.get("/get_users",response_model=List[res_user])
def get_users(db: Session = Depends(get_db)):
    #querying the database session
    data_users = db.query(models.User).all()
    return data_users

@app.get('/get_id/{user_id}',response_model = res_user)
def find_user(user_id:int, db: Session = Depends(get_db)):
    one_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if one_user == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the id is not found"))
    return one_user


