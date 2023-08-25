from bson import ObjectId
from datetime import datetime

from src.database import db
from src.db_constants import POSTS
from src.utils import get_paginated_list_of_items
from src.auth import get_user_id_from_token

from .models import PostCreateRequest, CommentCreateRequest


async def insert_post(post: PostCreateRequest, token: str):
    """
        Insert post in posts collection
    """
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
    """
        Returns post with matching post id if available.
    """
    post = db[POSTS].find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise ValueError("Invalid post id")
    return post


async def get_list_of_posts(page: int, size: int):
    """
        Return paginated list of posts data
    """
    skip = (page - 1) * size
    limit = size
    posts_list = await db[POSTS].find().skip(skip).limit(limit).to_list(None)
    total_records = await db[POSTS].count_documents({})

    for post in posts_list:
        post["_id"] = str(post["_id"])

    return await get_paginated_list_of_items(page=page, size=size, total_records=total_records, items=posts_list)


async def add_comment_on_a_post(post_id: str, comment: CommentCreateRequest, token: str):
    """
        Add comment to a post
    """
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
    """
        Return list of comments on a post
    """
    post = await db[POSTS].find_one({"_id": ObjectId(post_id)})
    print(post)
    comments_list = post["comments"]
    print(comments_list)

    return {"comments": comments_list}
