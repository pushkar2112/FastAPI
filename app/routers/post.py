from .. import models, schemas, oauth2
from typing import List
from fastapi import APIRouter, Body, FastAPI, Response, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Post']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    # curs.execute("select * from posts")
    # posts = curs.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    # We dont use fstrings coz they make us vulnerable to SQL injection attacks
    # curs.execute('insert into posts (title, content, published) values (%s,%s,%s) returning *',(post.title, post.content, post.published))
    # new_post = curs.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int, 
    response: Response, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    # curs.execute("select * from posts where id = %s",(str(id)))
    # post = curs.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post Not Found!!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found!!")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    # #deleting post
    # curs.execute("delete from posts where id = %s returning *",(str(id)))
    # deleted_post = curs.fetchone()

    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")
    
    post.delete(synchronize_session=False)
    db.commit()
    
# We do not return a message!
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int, 
    updated_post: schemas.PostUpdate, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    # curs.execute("update posts set title = %s, content = %s, published = %s where id = %s returning *",
    # (post.title, post.content, post.published, str(id)))
    
    # updated_post = curs.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()