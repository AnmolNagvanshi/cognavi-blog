from motor.motor_asyncio import AsyncIOMotorClient
from src.constants import config


client = AsyncIOMotorClient(config.MONGO_URI)
db = client[config.DATABASE_NAME]
