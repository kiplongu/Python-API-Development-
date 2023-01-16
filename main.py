from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

#pydantic model used to define how schema should look like 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#creating a variable to store data temporarily when no db is presesnt
my_posts=[{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": 
"favorite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def read_root():
    return {"message": "Welcome to my api dev journey for 22 days"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


#retrieving multiple posts
@app.post("/posts")
def create_posts(post: Post):
    post_dict= post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


#retrieving one individual post, the id field represents a path parameter

@app.get("/posts/{id}")
def get_post(id: int):    #add int to convert automatically into an integer
    Post = find_post(id)
    print(Post)
    return {"post_detail": Post}

# title str, content str, category, bool published