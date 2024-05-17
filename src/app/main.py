from typing import Any

from fastapi import Depends
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, get_db

"""below will create db tables if not exists in db when we start our project. If its already available it will create new tables.
If there is any change we did in models we need to first delete table from the db then only new table will be created with the changes.
"""
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    # optional fields below
    published: bool = True


@app.get("/")
async def root():
    return {"message": "Hello Worlds"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post, db: Session = Depends(get_db)) -> dict[str, Any]:
    new_post_dict = new_post.model_dump()  # converting payload to dict
    new_post_query = models.Post(**new_post_dict)  # unpacking dict(keys and values in query)
    db.add(new_post_query)
    db.commit()
    db.refresh(new_post_query)

    # return {"data ": new_post_query}  //this is throwing an exception
    return {"message": {
        "id": new_post_query.id,
        "title": new_post_query.title,
        "content": new_post_query.content,
        "published": new_post_query.published,
        "created_at": new_post_query.created_at
    }}


@app.get("/posts/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"Post with id {id} not found"})
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"No post can be found with this {id}. Please provide valid post id"})
    post_query.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, new_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"No post can be found with this {id}. Please provide valid post id"})
    else:
        post_dict = new_post.model_dump()
        post_query.update({
            **post_dict
        }, synchronize_session=False)
        db.commit()
        return {"status": "success"}
