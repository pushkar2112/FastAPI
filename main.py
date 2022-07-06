from turtle import title
from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my API!"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your post!"}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}