import jwt

from fastapi import Request, HTTPException
from constants import config
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(request: Request):
    """
        This function is used to protect routes from public access
        Usage Example: user=Depends(get_current_user)
    """

    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication Token not found"
        )
    else:
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



def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)

