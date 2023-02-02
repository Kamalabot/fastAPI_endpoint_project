#!/usr/bin/env python

##During the initial dev, the responses for each path was having object signature
## of {'name':data:Dict}. This is useful for knowing what the route is sending 
#back. After the initial dev, the program is cleaned and the additional indicators
#are removed

from fastapi import Depends, FastAPI,Response,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import models

from .routers import posts, users, auth, vote

#The ORM engine is created in separate file called database
from sqlalchemy.orm import Session
from .databaseORM import engine

#This line creates the tables through sqlalchemy. 
#However there is alembic now, doing this job. So the line is 
#commented out
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#the below origins can be https://www.google.com, https://www.youtube.com etc
origins  = ["*"]
app.add_middleware(
        CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
        )
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
