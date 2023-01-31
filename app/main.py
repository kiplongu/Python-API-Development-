from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


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


#code for testing

@app.get("/sqlalchemy")
def test_posts(db: Session= Depends(get_db)):
    return{"status": "success"}


@app.get("/posts")
def get_posts():
    # Execute a query
    cursor.execute(""" SELECT * FROM posts """)
    # Retrieve query results
    posts = cursor.fetchall()
    return {"data": posts}


#creating a post and the %s variable helps in securing against sql injection. also first %s goes with post.title etc

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


#retrieving one individual post, the id field represents a path parameter

@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute(""" SELECT * FROM posts WHERE id =%s""", (str(id)))
    Post = cursor.fetchone()
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
    cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post= cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#path operation for put/update request

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist") 

    return{"data": updated_post}
