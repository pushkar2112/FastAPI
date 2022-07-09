from time import time
from turtle import title
from typing import Optional
from fastapi import Body, FastAPI, Response, Depends, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    # Basically this ORM method makes a SQL quey to the db
    posts = db.query(models.Post).all()
    
    return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # curs.execute("select * from posts")
    # posts = curs.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # We dont use fstrings coz they make us vulnerable to SQL injection attacks
    # curs.execute('insert into posts (title, content, published) values (%s,%s,%s) returning *',(post.title, post.content, post.published))
    # new_post = curs.fetchone()
    # conn.commit()

    new_post = models.Post(title=post.title, content=post.content, published= post.published)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    curs.execute("select * from posts where id = %s",(str(id)))
    post = curs.fetchone()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post Not Found!!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found!!")
    return {"post_details": post} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    curs.execute("delete from posts where id = %s returning *",(str(id)))
    deleted_post = curs.fetchone()

    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")
    
# We do not return a message!
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    curs.execute("update posts set title = %s, content = %s, published = %s where id = %s returning *",
    (post.title, post.content, post.published, str(id)))
    
    updated_post = curs.fetchone()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")

    conn.commit()

    return {"data": updated_post}
