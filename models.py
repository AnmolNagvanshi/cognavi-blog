from typing import Union, List
from pydantic import BaseModel, Field
from utils import SerializedObjectId
from datetime import datetime
from bson import ObjectId
import pydantic


pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    id: str = Field(alias="_id")
    first_name: str
    last_name: str
    email: str
    access_token: str


class UserCreateRequest(BaseModel):
    """
        Request model class for creating single user
    """
    first_name: str
    last_name: str
    email: str
    password: str


class UserCreateResponse(BaseModel):
    """
        Response model class for creating single user
    """
    id: str = Field(alias="_id")
    first_name: str
    last_name: str
    email: str


class UserSingleResponse(BaseModel):
    """
        Response model class for retreiving single user by id
    """
    id: str = Field(alias="_id")
    first_name: str
    last_name: str
    email: str
    created_on: datetime


class UserListResponse(BaseModel):
    """
        Response model class for retrieving all users. Response is Paginated.
    """
    page: int
    size: int
    total_pages: int
    total_records: int
    items: List[UserSingleResponse]


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
