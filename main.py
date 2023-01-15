from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my api dev journey for 22 days"}


@app.get("/posts")
def get_posts():
    return {" data": "This is your posts rodgers"}

@app.post("/createposts")
def create_posts(payload: dict= Body(...)):
    print(payload)
    return {"new_post": f"title {payload['title']} content:{payload['content']}"}