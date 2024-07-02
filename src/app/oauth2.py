from datetime import datetime, timedelta

from jose import JWTError, jwt
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer

# directly pasted from the fastapi docs  https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=password
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

outh2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data : dict) -> str:
    data_to_encode = data.copy()
    expires_in = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expires_in})

    return jwt.encode(data_to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = schemas.TokenData(id)
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(outh2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"could not validate credentials",
                                          headers= {"WWW-Authenticate": "Bearer "})

    return verify_access_token(token, credentials_exception)




