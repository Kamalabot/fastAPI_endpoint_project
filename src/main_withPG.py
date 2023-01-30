#!/usr/bin/env python

#This is the trial script learning the fastapi library
from random import randint
# The import of Response, followed by Status and HTTPException were all 
# required for return appropriate response when the result is Null
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

#In order to enforce schema on the post requests following class is declared
class Newposts(BaseModel):
    title:str
    content:str
    category:int = 5
    rating:Optional[int] = None

app = FastAPI()

local_posts =[{"title":"post 1","content":"We have to work on the FastAPI very fast","id":1},
              {"title":"kafka kites","content":"There has never been a time like this","id":2}]

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
    return {"message":"Hello Fast world"}

#below handle informs path of the website
@app.get("/posts")
def get_posts():
    return {"YourPosts":"There you go. Your posts",
            "data":local_posts}
'''
#lets work on the POST request without pydantic
@app.post("/createposts")
def make_posts(payLoad: dict = Body):
    print(payLoad)
    return {"message":"SUCCESS"}
'''
'''
#lets work on the POST request withpydantic
@app.post("/createposts")
def make_pydanticposts(load: Newposts):
    print(load)
    print(f"The load title is {load.title}")
    return {"message":"Success with Pydantic","your post":load}
'''
#lets make createposts useful and load data into local_posts array

@app.post("/addposts",status_code=status.HTTP_201_CREATED)
def add_posts(load: Newposts):
    id_post = randint(0,5086268)
    #The Pydantic objects don't support the item assignment, so convert to dict
    post_data = load.dict()
    #Adding the updated id number
    post_data['id']=id_post
    #Appending the post to local array
    local_posts.append(post_data)
    #returning the response along with the array data
    return{"message":"post created",
           "updated posts": local_posts}
#The below route was pulled up in the file since fastapi will 
#resolve the "latest" wrongly
@app.get("/params/latest")
def get_recent():
    recent = local_posts[len(local_posts)-1]
    return {"recent":recent}

@app.get("/params/{prm}")
#Note the :int, this will validate the parameter
def print_params(prm :int, response: Response):
    print(prm)
    requestedPost = return_post(prm)
    if not requestedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The id {prm} is not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"hold on":f"The id {prm} is not found"}
    return {"message":"Got parameter","requested_post":requestedPost}

@app.delete("/delete/{id}",status_code = status.HTTP_204_NO_CONTENT)
#when using the 204 status, the remaining posts or any data cannot be sent
def delete_posts(id :int):
    get_idx = return_index_post(id)
    if get_idx == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the id is not found"))
    local_posts.pop(get_idx)
    #return {"msg":"post deleted","remaining posts":local_posts}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/{id}",status_code=status.HTTP_201_CREATED)
def update_post(id :int,post:Newposts):
    index = return_index_post(id)
    if index == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND))
    #Converting the recieved post into dictionary
    post_data = post.dict()

    #update the id in the recieved data and replace that in the local_posts

    post_data['id'] = id
    local_posts[index] = post_data
    return {'message':"data updated",
            "data":local_posts}

