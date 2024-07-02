from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from .. import utils

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    # we first need to hash the password
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password

    new_user_dict = new_user.model_dump()
    new_user_query = models.User(**new_user_dict)
    db.add(new_user_query)
    db.commit()
    db.refresh(new_user_query)
    return new_user_query


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": "Unable to find user user with userid {id}"})
    else:
        return user
