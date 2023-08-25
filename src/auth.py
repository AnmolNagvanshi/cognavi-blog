import jwt

from fastapi import Request, HTTPException
from src.constants import config


async def get_user_id_from_token(token):
    """
        Return user_id by decoding jwt token
    """
    token = token.replace("Bearer ", "")
    token_data = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
    return token_data["user_id"]


def get_current_user(request: Request):
    """
        This function is used to protect api routes from unauthenticated access
        Usage Example: user=Depends(get_current_user)
    """

    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication Token not found"
        )
    
    try:
        token = token.replace("Bearer ", "")
        token_data = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])

        if token_data:
            return True
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )
        
    except Exception as ex:
        print(f"Invalid token, exception = {str(ex)}")
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
