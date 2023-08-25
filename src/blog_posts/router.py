from fastapi import APIRouter, Request, Depends
from starlette.exceptions import HTTPException
from src.auth import get_current_user

from .models import (
    PostCreateRequest, PostCreateResponse, PostSingleResponse, PostListResponse,
    CommentCreateRequest, CommentCreateResponse, CommentsOnPostResponse
    )

from .service import (
    get_post_by_id, get_list_of_posts, get_list_of_comments_by_post_id,
    insert_post, add_comment_on_a_post
)


router = APIRouter()


@router.post("/posts", response_model=PostCreateResponse)
async def create_post(post: PostCreateRequest, request: Request, valid_user=Depends(get_current_user)):
    """
        Handles 'create post' api endpoint and creates new post in db.
    """
    try:
        token = request.headers.get("Authorization", None)        
        saved_post = await insert_post(post=post, token=token)
        return saved_post

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.get("/posts/{post_id}", response_model=PostSingleResponse)
async def get_single_post(post_id: str, valid_user=Depends(get_current_user)):
    """
        Handles 'get post by post id' endpoint. Returns the post if available.
    """
    try:
        post = await get_post_by_id(post_id=post_id)
        return post

    except ValueError as ex:
        raise HTTPException(status_code=406, detail="post with given id does not exist")
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.get("/posts", response_model=PostListResponse)
async def get_all_posts(page: int = 1, size: int = 20, valid_user=Depends(get_current_user)):
    """
        Handles 'get all posts made by a user' api. Returns paginated list of posts.
    """
    try:
        posts_list_paginated = await get_list_of_posts(page=page, size=size)
        return posts_list_paginated
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.post("/posts/{post_id}/comments", response_model=CommentCreateResponse)
async def create_comment_on_a_post(post_id: str, comment: CommentCreateRequest, request: Request, valid_user=Depends(get_current_user)):
    """
        Handles 'create comment on a post' api and creates new comment in db.
    """
    try:
        token = request.headers.get("Authorization", None)        
        saved_comment = await add_comment_on_a_post(post_id=post_id, comment=comment, token=token)
        return saved_comment
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.get("/posts/{post_id}/comments", response_model=CommentsOnPostResponse)
async def get_all_comments_on_a_post(post_id: str, valid_user=Depends(get_current_user)):
    """
        Handles 'get all comments made on a post' api. Returns list of comments.
    """
    try:
        comments_list = await get_list_of_comments_by_post_id(post_id=post_id)
        return comments_list
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")
