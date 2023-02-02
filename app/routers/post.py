from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )


#retriving many posts

@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session= Depends(get_db)):
    # Execute a query
    #cursor.execute(""" SELECT * FROM posts """)
    # Retrieve query results
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts


#creating a post and the %s variable helps in securing against sql injection. also first %s goes with post.title etc
#to make sur

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db), get_current_user:int= Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#retrieving one individual post, the id field represents a path parameter

@router.get("/{id}", response_model=schemas.Post)
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}", response_model=schemas.Post)
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

    