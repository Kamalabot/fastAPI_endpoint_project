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

@app.get("/sqlormtest")
def get_ormres(db: Session = Depends(get_db)):
    #querying the database session
    data_posts = db.query(models.Post).all()
    return {"db_post":data_posts}

#below handle informs path of the website
@app.get("/posts")
def get_posts():
    #Query the table 
    
    cur.execute("SELECT * FROM social_posts")
    
    #get the data into templist
    
    postsList = cur.fetchall()
    return {"YourPosts":"There you go. Your posts",
            "data":postsList}
#lets make createposts useful and load data into local_posts array

@app.post("/addposts",status_code=status.HTTP_201_CREATED)
def add_posts(load: Newposts):
    print(load)
    #Appending the post to local array
    cur.execute("""INSERT INTO social_posts(title, content, is_published)
                VALUES(%s, %s, %s) RETURNING * """,(load.title,load.content,
                                                     load.is_published))
    updated_post = cur.fetchone()
    #returning the response along with the array data
    return{"message":updated_post}

@app.get("/params/latest")
def get_recent():
    cur.execute("""SELECT * FROM social_posts 
                ORDER BY post_id DESC
                LIMIT 1""")
    recent_post = cur.fetchone()
    return {"Recent Post":recent_post}

@app.get("/params/{prm}")
#Note the :int, this will validate the parameter
def print_params(prm :int, response: Response):
    print(prm)
    #There is a gotcha here. The id has to be string when sending the query.
    #There is an extra comman after str(prm), for some reason!!!
    cur.execute("""SELECT * FROM social_posts WHERE post_id = %s""",(str(prm),))
    requestedPost = cur.fetchone()
    if not requestedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The id {prm} is not found')
    return {"message":"Got post","requested_post":requestedPost}

@app.delete("/delete/{id}",status_code = status.HTTP_204_NO_CONTENT)
#when using the 204 status, the remaining posts or any data cannot be sent
def delete_posts(id :int):
    cur.execute("""DELETE FROM social_posts WHERE post_id = %s RETURNING *""",(str(id))) 
    deleted = cur.fetchone()
    if deleted == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the id is not found"))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/{id}",status_code=status.HTTP_201_CREATED)
def update_post(id :int,post:Newposts):
    cur.execute("""UPDATE social_posts SET title = %s,content = %s WHERE post_id = %s RETURNING *""",
                 (post.title,post.content,str(id)))
    executed = cur.fetchone()
    if executed == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND))

    #update the id in the recieved data and replace that in the local_posts
    return {'message':"data updated",
            "data":executed} 
