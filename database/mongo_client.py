import os
from pymongo import MongoClient

class MongoDB:
    _client = None
    _db = None

    @classmethod
    def get_db(cls):
        mongo_uri = os.environ.get('MONGO_URI') or os.environ.get('MONGODB_URI')
        if not mongo_uri:
            return None
        
        if cls._db is None:
            cls._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000, connectTimeoutMS=3000)
            # Default database name is 'career_guidance' if not specified in URI path
            cls._db = cls._client.get_default_database(default='career_guidance')
        return cls._db


def get_mongo_db():
    return MongoDB.get_db()
