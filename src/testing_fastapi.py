#!/usr/bin/env python

#This is the trial script learning the fastapi library

from fastapi import FastAPI

super_app = FastAPI()

#below decorator informs path and http method
@super_app.get("/")
#async root function is initiated
def rooted():
    #When the root function is called the message is 
    #is returned.
    return {"lets Go":"Where to go? Fast world"}
