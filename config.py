import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'careerpath-ai-secret-key-2026-secure-default'
    
    # MongoDB Atlas Connection URI
    MONGO_URI = os.environ.get('MONGO_URI') or os.environ.get('MONGODB_URI')
    
    # Database URL handling
    raw_db_url = os.environ.get('DATABASE_URL')
    if raw_db_url and raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
        
    if raw_db_url:
        SQLALCHEMY_DATABASE_URI = raw_db_url
    else:
        # On Vercel / serverless read-only environment, write SQLite to /tmp
        if os.environ.get('VERCEL') or not os.access(BASE_DIR, os.W_OK):
            sqlite_path = '/tmp/career_guidance.db'
        else:
            sqlite_path = os.path.join(BASE_DIR, 'database', 'career_guidance.db')
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_path

    SQLALCHEMY_TRACK_MODIFICATIONS = False


