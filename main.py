from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def read_root():
    return {"message": "Welcome to my api dev journey for 22 days"}


@app.get("/posts")
def get_posts():
    return {" data": "This is your posts rodgers"}

@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return post

# title str, content str, category, bool published