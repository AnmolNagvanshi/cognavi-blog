from bson import ObjectId
from typing import List, Dict
import jwt
from constants import config


class SerializedObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


async def get_user_id_from_token(token):
    token = token.replace("Bearer ", "")
    token_data = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
    return token_data["user_id"]


async def get_paginated_list_of_items(page: int, size: int, total_records: int, items: List[Dict[str, str]]):

    total_pages = total_records // size
    if total_records % size != 0:
        total_pages += 1

    response = {
            "page": page,
            "size": size,
            "total_records": total_records,
            "total_pages": total_pages,
            "items": []
        }

    if total_records != 0:
        response["items"] = items
    
    return response
