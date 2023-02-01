
from fastapi import Depends, FastAPI,Response,status,HTTPException, APIRouter
from fastapi.params import Body
import time

from .. import models 
from ..comm_schema import res_post, create_post,req_post
from typing import List

#The ORM engine is created in separate file called database
from sqlalchemy.orm import Session
from ..databaseORM import get_db

router = APIRouter(
        prefix = '/posts',
        tags = ['Posts']
        )

#The other / has been deleted 
@router.get("/",response_model=List[res_post])
def get_ormres(db: Session = Depends(get_db)):
    #querying the database session
    data_posts = db.query(models.Post).all()
    return data_posts

#lets make createposts useful and load data into local_posts array

@router.post("/addposts",status_code=status.HTTP_201_CREATED,response_model=res_post)
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
@router.get("/params/latest")
def get_recent(db: Session = Depends(get_db)):
    data_posts = db.query(models.Post).order_by('post_id').all()
    return data_posts
'''

@router.get("/params/{prm}")
#Note the :int, this will validate the parameter
def print_params(prm :int, db: Session = Depends(get_db)):
    one_row = db.query(models.Post).filter(models.Post.post_id == prm).first()
    if not one_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The id {prm} is not found')
    return one_row

@router.delete("/delete/{id}",status_code = status.HTTP_204_NO_CONTENT)
#when using the 204 status, the remaining posts or any data cannot be sent
def delete_posts(id :int,db: Session = Depends(get_db)):
    one_row = db.query(models.Post).filter(models.Post.post_id == id) 
    if one_row.first() == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the id is not found"))
    one_row.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/update/{id}",status_code=status.HTTP_201_CREATED,response_model=res_post)
def update_post(id :int,post:create_post,db: Session = Depends(get_db)):
    save_query = db.query(models.Post).filter(models.Post.post_id == id)

    if save_query.first()== None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND))

    save_query.update(post.dict(),synchronize_session=False)
    db.commit()

    #update the id in the recieved data and replace that in the local_posts
    return save_query.first()


