import os
from hashlib import sha256
from sqlalchemy import create_engine


class Config:
    # Configuration
    JWT_SECRET_KEY = "COOL"  # Replace with your actual secret key
    BOT_TOKEN_HASH = sha256("7505659847:AAF3AoBU0HFInjsPPOqz4KaPmX3M15l9f1U".encode())  # Replace with your actual token
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@db:5432/cards"  # SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
    # SQLite proxy connection URL
    SQLITE_PROXY_URL = "sqlite:///tcp://sqlite-proxy:9000/"
    
    # Initialize engine at class level
    SQLITE_ENGINE = create_engine(
        SQLITE_PROXY_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30
    )
    
    # Or if you prefer lazy initialization:
    """
    _sqlite_engine = None
    
    @classmethod
    def get_sqlite_engine(cls):
        if cls._sqlite_engine is None:
            cls._sqlite_engine = create_engine(cls.SQLITE_PROXY_URL)
        return cls._sqlite_engine
    """