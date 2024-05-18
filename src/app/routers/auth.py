from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, utils, oauth2
"""Instead of passing user credentials from body we can use fastapi feature
    OAuth2PasswordRequestForm will only return dict with 2 fields username and password
    in our case email will be assigned to username field
"""

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authorization"]
)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    # here we will create token and return it
    # return {"message": "authentication successful"}

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}


