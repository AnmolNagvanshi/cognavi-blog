import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv(verbose=True)

class GlobalConfig(BaseSettings):
    """
        Global config variables
    """

    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')

    MONGO_URI: str = os.getenv('MONGO_URI')
    DATABASE_NAME: str = os.getenv('DATABASE_NAME')


@lru_cache()
def get_global_config():
    return GlobalConfig()


config = get_global_config()