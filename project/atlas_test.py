from dotenv import load_dotenv
from pathlib import Path
import os
from pymongo import MongoClient

load_dotenv(Path(__file__).resolve().parent / ".env")

uri = os.getenv("MONGO_URI")
print("URI:", uri)

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
client.admin.command("ping")

print("✅ Atlas connection successful")
