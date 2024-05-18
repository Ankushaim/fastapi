from fastapi import FastAPI

from . import models
from .database import engine
from .routers import posts, users, auth

"""below will create db tables if not exists in db when we start our project. If its already available it will create new tables.
If there is any change we did in models we need to first delete table from the db then only new table will be created with the changes.
"""
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello Worlds"}