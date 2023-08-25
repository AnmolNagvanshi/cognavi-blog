from typing import List, Dict
from src.constants import config


async def get_paginated_list_of_items(page: int, size: int, total_records: int, items: List[Dict[str, str]]):
    """
        Returns formatted response payload for paginated list of items
    """

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
