from bson import ObjectId
from datetime import datetime, timedelta
from typing import Union
import jwt

from database import db
from db_constants import USERS, POSTS
from auth import get_password_hash, verify_password
from utils import get_paginated_list_of_items, get_user_id_from_token
from constants import config

from models import (
    LoginRequest,
    UserCreateRequest, 
    PostCreateRequest, 
    CommentCreateRequest
    )


async def login_user_service(user: LoginRequest):
    user = user.dict()
    email = user["email"]
    password = user["password"]

    user_data = await db[USERS].find_one({"email": email})
    if user_data is None:
        raise ValueError("Invalid user email")
    
    if not verify_password(password,  user_data["password"]):
        raise ValueError("Password mismatch")
    
    user_data["_id"] = str(user_data["_id"])

    payload = {
        'user_id': user_data["_id"],
        'exp': datetime.utcnow() + timedelta(hours=12)  # Token expiration time
    }

    # Generate the access token
    access_token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')
    user_data["access_token"] = access_token

    return user_data


async def insert_user(user: UserCreateRequest):
    user = user.dict()
    user["password"] = get_password_hash(user["password"])
    user["created_on"] = datetime.utcnow()

    inserted_user = await db[USERS].insert_one(user)
    print("Inserted user", inserted_user)

    saved_user = await db[USERS].find_one({"_id": inserted_user.inserted_id})
    saved_user["_id"] = str(saved_user["_id"])
    return saved_user



async def get_user_by_email(email: str):
    user = db[USERS].find_one({"email": email})
    if user is None:
        raise ValueError("Invalid user email")
    return user


async def get_user_by_id(user_id: str):
    print(user_id)
    user = await db[USERS].find_one({"_id": ObjectId(user_id)})
    print(user)
    if user is None:
        raise ValueError("Invalid user id")
    
    user["_id"] = str(user["_id"])
    return user


async def get_list_of_users(page: int, size: int):
    skip = (page - 1) * size
    limit = size
    user_list = await db[USERS].find().skip(skip).limit(limit).to_list(None)
    total_records = await db[USERS].count_documents()
    return await get_paginated_list_of_items(page=page, size=size, total_records=total_records, items=user_list)
    

async def insert_post(post: PostCreateRequest, token: str):
    post = post.dict()
    post["user_id"] = await get_user_id_from_token(token)
    post["comments"] = []
    post["created_on"] = datetime.utcnow()

    inserted_post = await db[POSTS].insert_one(post)
    print("Inserted post", inserted_post)

    saved_post = await db[POSTS].find_one({"_id": inserted_post.inserted_id})
    saved_post["_id"] = str(saved_post["_id"])
    return saved_post


async def get_post_by_id(post_id: str):
    post = db[POSTS].find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise ValueError("Invalid post id")
    return post


async def get_list_of_posts(page: int, size: int):
    skip = (page - 1) * size
    limit = size
    posts_list = await db[POSTS].find().skip(skip).limit(limit).to_list(None)
    total_records = await db[POSTS].count_documents({})

    for post in posts_list:
        post["_id"] = str(post["_id"])

    return await get_paginated_list_of_items(page=page, size=size, total_records=total_records, items=posts_list)



async def add_comment_on_a_post(post_id: str, comment: CommentCreateRequest, token: str):
    comment = comment.dict()
    comment["user_id"] = await get_user_id_from_token(token)
    comment["created_on"] = datetime.utcnow()

    post = await db[POSTS].find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise ValueError("Invalid post id, cannot comment on it")
    
    comments_list_on_post = [] if "comments" not in post else post["comments"]
    comments_list_on_post.append(comment)

    updated_post = await db[POSTS].update_one({"_id": ObjectId(post_id)}, {"$set": {"comments": comments_list_on_post}})
    return comment


async def get_list_of_comments_by_post_id(post_id: str):
    post = await db[POSTS].find_one({"_id": ObjectId(post_id)})
    print(post)
    comments_list = post["comments"]
    print(comments_list)

    return {"comments": comments_list}





