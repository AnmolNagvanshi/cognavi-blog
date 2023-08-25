from fastapi import APIRouter
from src.blog_users.router import router as users_router
from src.blog_posts.router import router as posts_router


api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(posts_router)
