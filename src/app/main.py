import time
from typing import Optional

import psycopg2
from fastapi import FastAPI, status, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastApiLearning", user="postgres", password="root",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print("Database connection established")
        break
    except Exception as e:
        print("Failed to connect")
        print(e)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    # optional fields below
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello Worlds"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post) -> dict[str, str]:
    cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (new_post.title, new_post.content, new_post.published))
    new_created_post = cursor.fetchone()
    conn.commit()
    return {"data ": f"{new_created_post}"}


@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"Post with id {id} not found"})
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"No post can be found with this {id}. Please provide valid post id"})


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, new_post: Post):
    cursor.execute(""" UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (new_post.title, new_post.content, new_post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"No post can be found with this {id}. Please provide valid post id"})
    else:
        return {"updated_post": updated_post}

# Test commit
