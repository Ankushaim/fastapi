from datetime import datetime, timedelta

from jose import JWTError, jwt

# directly pasted from the fastapi docs  https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=password
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data : dict) -> str:
    data_to_encode = data.copy()
    expires_in = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expires_in})

    return jwt.encode(data_to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
