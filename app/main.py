from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


#pydantic model used to define how schema should look like 


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

#retriving many posts

@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session= Depends(get_db)):
    # Execute a query
    #cursor.execute(""" SELECT * FROM posts """)
    # Retrieve query results
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts


#creating a post and the %s variable helps in securing against sql injection. also first %s goes with post.title etc

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#retrieving one individual post, the id field represents a path parameter

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session= Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id =%s""", (str(id)))
    # Post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    return  post


#deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session= Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post= cursor.fetchone()
    # conn.commit()
    post= db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)


#path operation for put/update request

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session= Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post== None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist") 

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

    #defining functionalities for users

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate, db: Session= Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
