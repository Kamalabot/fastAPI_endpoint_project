#!/usr/bin/env python

##During the initial dev, the responses for each path was having object signature
## of {'name':data:Dict}. This is useful for knowing what the route is sending 
#back. After the initial dev, the program is cleaned and the additional indicators
#are removed

from fastapi import Depends, FastAPI,Response,status,HTTPException

from . import models

from .routers import posts, users, auth

#The ORM engine is created in separate file called database
from sqlalchemy.orm import Session
from .databaseORM import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
