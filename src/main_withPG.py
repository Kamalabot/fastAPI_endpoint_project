#!/usr/bin/env python

#This is the mail script where the PG database connectivity is implemented 
from random import randint
# The import of Response, followed by Status and HTTPException were all 
# required for return appropriate response when the result is Null
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import time
import psycopg2
from psycopg2.extras import RealDictCursor

import configparser

creden = configparser.ConfigParser()
creden.read_file(open('calter.config'))

host = creden["LOCALPG"]["PG_HOST"]
database = creden["LOCALPG"]["PG_DB_FAST"]
port = creden["LOCALPG"]["PG_PORT"]
passwd = creden["LOCALPG"]["PG_PASS"]
user = creden["LOCALPG"]["PG_UNAME"]

#In order to retry the connection before the server starts the while loop is used
while True:
    try:
        conn = psycopg2.connect(host=host,
                        dbname=database,user=user,
                        password=passwd,port=port,
                            cursor_factory=RealDictCursor)

        conn.set_session(autocommit=True)

        cur = conn.cursor()
        print("connection established...")
        break

    except Exception as e:
        print(e)
        time.sleep(2)

#In order to enforce schema on the post requests following class is declared
class Newposts(BaseModel):
    title:str
    content:str
    is_published: bool = True

#Initiate the connection with postgres database 


app = FastAPI()

def return_post(ide):
    """This function returns the matching posts"""
    data = ''
    print('this is insider the return post function',ide)
    #Note the type of the ide has to be string for the condition to match
    for p in local_posts:
        if p["id"] == int(ide):
            print(p)
            data = p
    return data

def return_index_post(ide):
    """This function will pop the index of the element with the corresponding id"""
    for i, post in enumerate(local_posts):
        if post["id"] == ide:
            return i

#below decorator informs path and http method
@app.get("/")
#async root function is initiated
async def root():
    #When the root function is called the message is 
    #is returned.
    return {"db_server":"This is from Database Server"}

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
