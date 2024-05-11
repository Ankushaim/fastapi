from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    # defining two optional fields one with out using library and one using Optional from typing library
    published: bool = True
    rating: Optional[int] = None
    



@app.get("/")
async def root():
    return {"message": "Hello Worlds"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your posts"}


@app.post("/posts")
# def create_post(payload: dict = Body(...)):
# lets use Pydantic here. Arguments new_post is refrence and Post is model name   
def create_post(new_post: Post):
    print(new_post)

    # we can also convert pydantic model to dictionary
    print(new_post.model_dump())
          

    return {"data ": f"{new_post}"}