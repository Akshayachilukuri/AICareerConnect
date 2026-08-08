import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env'))

class Config:
    """Central configuration class for AI Career Connect."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-ai-career-connect-2026'
    
    # Database configuration - use /tmp on Render (ephemeral filesystem)
    root_dir = os.path.dirname(basedir)
    if os.environ.get('RENDER'):
        instance_dir = '/tmp/instance'
    else:
        instance_dir = os.path.join(root_dir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    db_path = os.path.join(instance_dir, 'app.db').replace('\\', '/')

    # SQLite Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mistral AI API Configuration
    MISTRAL_API_KEY = os.environ.get('MISTRAL_API_KEY') or ''
    MISTRAL_MODEL = 'mistral-small-latest'
    
    # File upload configurations - use /tmp on Render
    if os.environ.get('RENDER'):
        UPLOAD_FOLDER = '/tmp/uploads'
    else:
        UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
