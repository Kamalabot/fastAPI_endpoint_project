#!/usr/bin/env python

#This is the trial script learning the fastapi library

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

#In order to enforce schema on the post requests following class is declared
class Newposts(BaseModel):
    title:str
    content:str
    category:int

app = FastAPI()

#below decorator informs path and http method
@app.get("/")
#async root function is initiated
async def root():
    #When the root function is called the message is 
    #is returned.
    return {"message":"Hello Fast world"}

#below handle informs path of the website
@app.get("/posts")
def get_posts():
    return {"YourPosts":"There you go. Your posts"}
'''
#lets work on the POST request without pydantic
@app.post("/createposts")
def make_posts(payLoad: dict = Body):
    print(payLoad)
    return {"message":"SUCCESS"}
'''

#lets work on the POST request withpydantic
@app.post("/createposts")
def make_pydanticposts(load: Newposts):
    print(load)
    print(f"The load title is {load.title}")
    return {"message":"Success with Pydantic","your post":load}
