import os
from pymongo import MongoClient

class MongoDB:
    _client = None
    _db = None
    _disabled = False

    @classmethod
    def get_db(cls):
        if cls._disabled:
            return None

        mongo_uri = os.environ.get('MONGO_URI') or os.environ.get('MONGODB_URI')
        if not mongo_uri:
            return None
        
        if cls._db is None:
            try:
                cls._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1000, connectTimeoutMS=1000)
                cls._client.admin.command('ping')
                cls._db = cls._client.get_default_database(default='career_guidance')
            except Exception:
                cls._disabled = True
                return None
        return cls._db


def get_mongo_db():
    return MongoDB.get_db()
