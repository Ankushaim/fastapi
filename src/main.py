from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Worlds"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your posts"}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new post ": f"title: {payload['title']} content: {payload['content']} "}