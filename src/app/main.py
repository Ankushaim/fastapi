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


def find_index_of_post(id: int) -> int:
    print(id, type(id))
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return -1


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_index_of_post(id)
    print("post Index:", post_index)
    if post_index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"No post can be found with this {id}. Please provide valid post id"})
    else:
        my_posts.pop(post_index)



@app.put("/posts/{id}", status_code= status.HTTP_202_ACCEPTED)
def update_post(id: int, new_post: Post):
    print(id)
    post_index = find_index_of_post(id)

    if post_index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"message": f"No post can be found with this {id}. Please provide valid post id"})
    else:
        new_post_dict = new_post.model_dump()
        
        new_post_dict["id"] = id
        my_posts[post_index] = new_post_dict
        return {"data": new_post_dict}
        