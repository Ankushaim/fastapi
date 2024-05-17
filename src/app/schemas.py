from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass

    class Config:
        extra = "forbid"     # this will stop user to provide extra fields in request body.


class PostResponse(PostBase):
    created_at: datetime

    class Config:
        # this is deprecated we need to use below line. This will tell fastapi to convert orm object to dict
        # orm_mode = True
        from_attributes = True
