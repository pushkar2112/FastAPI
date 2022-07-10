from time import time
from turtle import title
from typing import Optional, List
from fastapi import Body, FastAPI, Response, Depends, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

my_posts = [
    {"title": "title of post1", "content": "content of post 1", "id": 1}, 
    {"title": "favourite foods", "content": "I like pizza!!", "id": 2}
    ]

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="Pushkar1", cursor_factory=RealDictCursor)
        curs = conn.cursor()
        print("Connected Successfully!")
        break
    except Exception as err:
        print("Connection failed!")
        print("ERROR: ", err)
        time.sleep(2)


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def root():
    return {"message": "Welcome to my API!"}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # curs.execute("select * from posts")
    # posts = curs.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # We dont use fstrings coz they make us vulnerable to SQL injection attacks
    # curs.execute('insert into posts (title, content, published) values (%s,%s,%s) returning *',(post.title, post.content, post.published))
    # new_post = curs.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # curs.execute("select * from posts where id = %s",(str(id)))
    # post = curs.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post Not Found!!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found!!")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
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

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
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

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password = user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist!")

    return user

