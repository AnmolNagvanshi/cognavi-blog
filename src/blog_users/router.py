from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from src.auth import get_current_user

from .models import (
    LoginRequest, LoginResponse,
    UserCreateRequest, UserCreateResponse, UserSingleResponse, UserListResponse,
    )

from .service import (
    get_user_by_id, get_user_by_email, get_list_of_users,
    insert_user, login_user_service
)


router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login_user(user_details: LoginRequest):
    """
        Handles 'login authentication' api for the user. Returns access token if verified.
    """
    try:
        user = await login_user_service(user=user_details)
        return user
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.post("/users", response_model=UserCreateResponse)
async def create_user(user: UserCreateRequest):
    """
        Handle 'create user' api and creates new user in db.
    """
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
    """
        Handles 'get user by user_id' api. Return user if available.
    """
    try:
        user = await get_user_by_id(user_id=user_id)
        return user

    except ValueError as ex:
        raise HTTPException(status_code=406, detail="user with given id does not exist")
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")


@router.get("/users", response_model=UserListResponse)
async def get_all_users(page: int = 1, size: int = 20, valid_user=Depends(get_current_user)):
    """
        Handles 'get all users' api. Return paginated list of users from db.
    """
    try:
        users_list_paginated = await get_list_of_users(page=page, size=size)
        return users_list_paginated

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception occured: {ex}")