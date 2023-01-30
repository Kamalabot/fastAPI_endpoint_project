#!/usr/bin/env python

#This is the trial script learning the fastapi library

from fastapi import FastAPI

app = FastAPI()

#below decorator informs path and http method
@app.get("/")
#async root function is initiated
async def root():
    #When the root function is called the message is 
    #is returned.
    return {"message":"Hello Fast world"}

#below handle informs path of the website
@app.get("/intuit")
async def intuit():
    return {"yourIntution":"When you can intuit, you love programming."}
