from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


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



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to my api dev journey for 22 days"}

