from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from ..database import get_db

router = APIRouter(
    prefix= "/posts",
    tags= ["Post"],
)




@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(new_post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post_dict = new_post.model_dump()  # converting payload to dict
    new_post_query = models.Post(**new_post_dict)  # unpacking dict(keys and values in query)
    db.add(new_post_query)
    db.commit()
    db.refresh(new_post_query)
    return new_post_query


@router.get("/{id}", response_model=schemas.PostResponse)
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"Post with id {id} not found"})
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"No post can be found with this {id}. Please provide valid post id"})
    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id: int, new_post: schemas.CreatePost, db: Session = Depends(get_db)):
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
        return post_query.first()
