from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
import pydantic


pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


class PostCreateRequest(BaseModel):
    """
        Request model class for creating single post
    """
    title: str
    content: str


class PostCreateResponse(BaseModel):
    """
        Response model class for creating single post
    """
    id: str = Field(alias="_id")
    title: str
    content: str
    user_id: str
    

class PostSingleResponse(BaseModel):
    """
        Response model class for retrieving single post by id
    """
    id: str = Field(alias="_id")
    title: str
    content: str
    user_id: str
    created_on: datetime  # datetime


class PostListResponse(BaseModel):
    """
        Response model class for retrieving all posts. Response is Paginated.
    """
    page: int
    size: int
    total_pages: int
    total_records: int
    items: List[PostSingleResponse]



class CommentCreateRequest(BaseModel):
    """
        Request model class for creating comment on a post
    """
    content: str


class CommentCreateResponse(BaseModel):
    """
        Response model class for creating comment on a post
    """
    content: str
    user_id: str
    created_on: datetime


class CommentsOnPostResponse(BaseModel):
    """
        Response model class for retrieving all comments on a single post
    """
    comments: List[CommentCreateResponse]
