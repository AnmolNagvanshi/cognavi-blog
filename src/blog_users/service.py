from bson import ObjectId
from datetime import datetime, timedelta
import jwt

from src.database import db
from src.db_constants import USERS
from .utils import get_password_hash, verify_password
from src.constants import config
from src.utils import get_paginated_list_of_items


from .models import LoginRequest, UserCreateRequest


async def login_user_service(user: LoginRequest):
    """
        Verifies user and return access token to the user if authenticated.
    """
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
    """
        Creates new user in db
    """
    user = user.dict()
    user["password"] = get_password_hash(user["password"])
    user["created_on"] = datetime.utcnow()

    inserted_user = await db[USERS].insert_one(user)
    print("Inserted user", inserted_user)

    saved_user = await db[USERS].find_one({"_id": inserted_user.inserted_id})
    saved_user["_id"] = str(saved_user["_id"])
    return saved_user


async def get_user_by_email(email: str):
    """
        Returns user with matching email if available.
    """
    user = db[USERS].find_one({"email": email})
    if user is None:
        raise ValueError("Invalid user email")
    return user


async def get_user_by_id(user_id: str):
    """
        Returns user with matching user_id if available.
    """
    print(user_id)
    user = await db[USERS].find_one({"_id": ObjectId(user_id)})
    print(user)
    if user is None:
        raise ValueError("Invalid user id")
    
    user["_id"] = str(user["_id"])
    return user


async def get_list_of_users(page: int, size: int):
    """
        Returns paginated list of users present in db.
    """
    skip = (page - 1) * size
    limit = size
    user_list = await db[USERS].find().skip(skip).limit(limit).to_list(None)
    total_records = await db[USERS].count_documents()
    return await get_paginated_list_of_items(page=page, size=size, total_records=total_records, items=user_list)
