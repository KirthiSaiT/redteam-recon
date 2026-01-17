from motor.motor_asyncio import AsyncIOMotorClient
import os

import certifi

# Connection String
MONGODB_URL = "mongodb+srv://kirthisai251_db_user:Omk2yu8KNjcQe0Ob@cluster0.dqel6xf.mongodb.net/?appName=Cluster0"

client = AsyncIOMotorClient(MONGODB_URL, tlsAllowInvalidCertificates=True)
db = client.recon_db
scan_collection = db.scans

async def get_database():
    return db
