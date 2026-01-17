import asyncio
import sys
import os

# Add app to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.subdomain import SubdomainService
from app.database import scan_collection, get_database

async def test_mongo():
    print("Testing MongoDB Connection...")
    try:
        db = await get_database()
        print("MongoDB Connection Successful:", db.name)
        count = await scan_collection.count_documents({})
        print(f"Current scans in DB: {count}")
    except Exception as e:
        print(f"MongoDB Failed: {e}")

def test_subdomains():
    print("\nTesting Subdomain Discovery (crt.sh)...")
    try:
        subs = SubdomainService.get_subdomains_crtsh("volvo.com")
        print(f"Found {len(subs)} subdomains.")
        if len(subs) > 0:
            print(f"Sample: {subs[:3]}")
    except Exception as e:
        print(f"Subdomain Discovery Failed: {e}")

if __name__ == "__main__":
    test_subdomains()
    asyncio.run(test_mongo())
