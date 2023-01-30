#!/usr/bin/env python

#This is the mail script where the PG database connectivity is implemented 
# required for return appropriate response when the result is Null
from fastapi import Depends, FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import time

from sqlalchemy.orm import Session
#The name of the supporting models python file has to be models.py
from . import models
#The ORM engine is created in separate file called database
from .databaseORM import engine, get_db 

models.Base.metadata.create_all(bind=engine)

class Newposts(BaseModel):
    title:str
    content:str
    is_published: bool = True

app = FastAPI()

#below decorator informs path and http method
@app.get("/")
#async root function is initiated
async def root():
    #When the root function is called the message is 
    #is returned.
    return {"db_server":"This is from Database Server"}

#The other /posts has been deleted 
@app.get("/posts")
def get_ormres(db: Session = Depends(get_db)):
    #querying the database session
    data_posts = db.query(models.Post).all()
    return {"db_post":data_posts}

#lets make createposts useful and load data into local_posts array

@app.post("/addposts",status_code=status.HTTP_201_CREATED)
def add_posts(load: Newposts,db: Session = Depends(get_db)):

#**load.dict() will take care of converting the variables in the format models will accept
    new_post = models.Post(**load.dict())
    #new_post = models.Post(title=load.title, content=load.content, is_published=load.is_published)
#need to present the query to engine
    db.add(new_post)
#query needs to be comitted
    db.commit()
#After that the refreshed database needs to be stored back in to the variable
    db.refresh(new_post)
    return{"message":new_post}

@app.get("/params/latest")
def get_recent(db: Session = Depends(get_db)):
    data_posts = db.query(models.Post).order_by('post_id').all()
    return {"Recent Post":data_posts}

@app.get("/params/{prm}")
#Note the :int, this will validate the parameter
def print_params(prm :int, db: Session = Depends(get_db)):
    one_row = db.query(models.Post).filter(models.Post.post_id == prm).first()
    if not one_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The id {prm} is not found')
    return {"message":"Got post","requested_post":one_row}

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

@app.put("/update/{id}",status_code=status.HTTP_201_CREATED)
def update_post(id :int,post:Newposts,db: Session = Depends(get_db)):
    save_query = db.query(models.Post).filter(models.Post.post_id == id)
    if save_query.first()== None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND))

    save_query.update(post.dict(),synchronize_session=False)
    db.commit()

    #update the id in the recieved data and replace that in the local_posts
    return {'message':"data updated",
            "data":save_query.first()} 
