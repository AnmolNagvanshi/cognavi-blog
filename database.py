from motor.motor_asyncio import AsyncIOMotorClient
from constants import config
import pymongo

client = AsyncIOMotorClient(config.MONGO_URI)
db = client[config.DATABASE_NAME]
