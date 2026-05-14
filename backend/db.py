import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

admins_collection = db["admins"]
history_collection = db["history"]
users_collection = db["users"]


history_collection.create_index("vehicle_number")
users_collection.create_index("email", unique=True)
