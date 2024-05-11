from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    # defining two optional fields one with out using library and one using Optional from typing library
    published: bool = True
    rating: Optional[int] = None
    

my_posts =[
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1,
    },
    {
        "title": "favourite foods",
        "content": "I like pizza",
        "id": 2,
    }
]

@app.get("/")
async def root():
    return {"message": "Hello Worlds"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# @app.post("/posts")
# def create_post(payload: dict = Body(...)):
# lets use Pydantic here. Arguments new_post is refrence and Post is model name


# default status code of created post is 200 but as per defination it should be 201. To change default status code please follow below
# @app.post("/posts")

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(2, 1000000)
    my_posts.append(post_dict)    
    return {"data ": f"{post_dict}"}


def find_post(id: int) -> dict:
    for post in my_posts:
        if post["id"] == id:
            return post


@app.get("/posts/{id}")
# def get_posts(id: int, response: Response):
def get_posts(id: int):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : "Post with id {id} not found"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message" : f"Post with id {id} not found"})
    
    return {"post_details": f"{post}"}