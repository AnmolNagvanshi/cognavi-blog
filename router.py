from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from auth import get_current_user, get_password_hash, verify_password


from models import (
    LoginRequest, LoginResponse,
    UserCreateRequest, UserCreateResponse, UserSingleResponse, UserListResponse,
    PostCreateRequest, PostCreateResponse, PostSingleResponse, PostListResponse,
    CommentCreateRequest, CommentCreateResponse, CommentsOnPostResponse
    )

from service import (
    get_post_by_id, get_list_of_posts, get_list_of_comments_by_post_id, get_user_by_id, get_user_by_email, get_list_of_users,
    insert_post, insert_user, add_comment_on_a_post, login_user_service
)


router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login_user(user_details: LoginRequest):
    try:
        user = await login_user_service(user=user_details)
        return user
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.post("/users", response_model=UserCreateResponse)
async def create_user(user: UserCreateRequest):
    try:
        user_dict = user.dict()
        user_data = await get_user_by_email(email=user_dict["email"])
        if user_data is not None:
            raise ValueError()
        
        saved_user = await insert_user(user=user)
        return saved_user
    
    except ValueError as ex:
        raise HTTPException(status_code=406, detail="user already exists")
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")
    


@router.get("/users/{user_id}", response_model=UserSingleResponse)
async def get_single_user(user_id: str, valid_user=Depends(get_current_user)):
    try:
        user = await get_user_by_id(user_id=user_id)
        return user

    except ValueError as ex:
        raise HTTPException(status_code=406, detail="user with given id does not exist")
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.get("/users", response_model=UserListResponse)
async def get_all_users(page: int = 1, size: int = 20, valid_user=Depends(get_current_user)):
    try:
        users_list_paginated = await get_list_of_users(page=page, size=size)
        return users_list_paginated

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")



@router.post("/posts", response_model=PostCreateResponse)
async def create_post(post: PostCreateRequest, request: Request, valid_user=Depends(get_current_user)):
    try:
        token = request.headers.get("Authorization", None)        
        saved_post = await insert_post(post=post, token=token)
        return saved_post

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.get("/posts/{post_id}", response_model=PostSingleResponse)
async def get_single_post(post_id: str, valid_user=Depends(get_current_user)):
    try:
        post = await get_post_by_id(post_id=post_id)
        return post

    except ValueError as ex:
        raise HTTPException(status_code=406, detail="post with given id does not exist")
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.get("/posts", response_model=PostListResponse)
async def get_all_posts(page: int = 1, size: int = 20, valid_user=Depends(get_current_user)):
    try:
        posts_list_paginated = await get_list_of_posts(page=page, size=size)
        return posts_list_paginated
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")



@router.post("/posts/{post_id}/comments", response_model=CommentCreateResponse)
async def create_comment_on_a_post(post_id: str, comment: CommentCreateRequest, request: Request, valid_user=Depends(get_current_user)):
    try:
        token = request.headers.get("Authorization", None)        
        saved_comment = await add_comment_on_a_post(post_id=post_id, comment=comment, token=token)
        return saved_comment
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.get("/posts/{post_id}/comments", response_model=CommentsOnPostResponse)
async def get_all_comments_on_a_post(post_id: str, valid_user=Depends(get_current_user)):
    try:
        comments_list = await get_list_of_comments_by_post_id(post_id=post_id)
        return comments_list
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")

