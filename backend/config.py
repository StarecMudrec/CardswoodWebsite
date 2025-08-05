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
    
    # For the TCP proxy we set up earlier
    SQLITE_PROXY_URL = "sqlite:///tcp://sqlite-proxy:9000/"  # Using container name
    # OR if using host networking:
    # SQLITE_PROXY_URL = "sqlite:///tcp://localhost:9000/"
    
    @property
    def SQLITE_ENGINE(self):
        if not hasattr(self, '_sqlite_engine'):
            self._sqlite_engine = create_engine(self.SQLITE_PROXY_URL)
        return self._sqlite_engine