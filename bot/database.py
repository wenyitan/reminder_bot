import sqlite3
from bot.config import TABLE_NAME, MONGO_URI, MONGO_DB, env
from pymongo import MongoClient

class Database:
    def __init__(self, mongo_uri=MONGO_URI):
        client = MongoClient(mongo_uri)
        db = client[MONGO_DB]
        self.collection = db[f"reminders_{env.lower()}"]
        print(f"Database connection initialised for {env.lower()}")