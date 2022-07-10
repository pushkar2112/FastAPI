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
from .routers import post, user

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

# We make router to seperate out the code in pur file
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API!"}



