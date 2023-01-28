from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

#pydantic model used to define how schema should look like 

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
   
   
   #seting up db connection after installing psycopg a adapter for posgresql, used for API implementation
while True:

    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '  ', cursor_factory=RealDictCursor)

    # Open a cursor to perform database operations
        cursor= conn.cursor()
        print("Database connection was succesful!")
        break
    except Exception as error:
        time.sleep(3)
        print("Database connection failed!")
        print("Error:", error)




#creating a variable to store data temporarily when no db is presesnt

my_posts=[{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": 
"favorite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p ["id"] == id:
            return i




@app.get("/")
def read_root():
    return {"message": "Welcome to my api dev journey for 22 days"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


#creating a post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict= post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


#retrieving one individual post, the id field represents a path parameter

@app.get("/posts/{id}")
def get_post(id: int, response: Response):    
    Post = find_post(id)
    if not Post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    return {"post_detail": Post}


#deleting post
#find the endex in the array that has required ID
#my_post.pop(index)-- for deleting

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#path operation for put/update request

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist") 
    post_dict= post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return{"data":post_dict}

    print(post)
    return{"message": "updated post"}

# title str, content str, category, bool published