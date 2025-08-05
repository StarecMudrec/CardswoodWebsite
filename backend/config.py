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
    
    # New SQLite engine (read-only)
    SQLITE_DB_PATH = "sqlite:////db/offcardswood.db?mode=ro"  # Read-only mode
    SQLITE_ENGINE = create_engine(SQLITE_DB_PATH)