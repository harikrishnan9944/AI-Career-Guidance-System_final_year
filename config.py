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
        
    SQLALCHEMY_DATABASE_URI = raw_db_url or \
        'sqlite:///' + os.path.join(BASE_DIR, 'database', 'career_guidance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

