import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:2135@localhost:5432/audioink_prod')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    STORAGE_PATH = os.getenv('STORAGE_PATH', 'data')
    MODEL_PATH = os.getenv('MODEL_PATH', 'models')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16777216'))  # 16MB default
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'mp3,wav,ogg,mp4,m4a,mpeg,webm').split(','))
    
    # GPU Configuration
    CUDA_VISIBLE_DEVICES = os.getenv('CUDA_VISIBLE_DEVICES', '0')
    GPU_MEMORY_FRACTION = float(os.getenv('GPU_MEMORY_FRACTION', '0.8'))
    
    # Gunicorn Configuration
    WORKERS = int(os.getenv('WORKERS', '4'))
    TIMEOUT = int(os.getenv('TIMEOUT', '120'))
    MAX_REQUESTS = int(os.getenv('MAX_REQUESTS', '1000'))
    MAX_REQUESTS_JITTER = int(os.getenv('MAX_REQUESTS_JITTER', '50'))

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'postgresql://postgres:2135@localhost:5432/audioink_dev')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:2135@localhost:5432/audioink_test')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:2135@localhost:5432/audioink_prod')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 