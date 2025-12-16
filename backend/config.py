import os
from hashlib import sha256
from sqlalchemy import create_engine

class Config:
    # Configuration
    JWT_SECRET_KEY = "COOL"  # Replace with your actual secret key

    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set")
    
    BOT_TOKEN_HASH = sha256(BOT_TOKEN.encode())

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@db:5432/cards"  # SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    # PayAnyWay / MONETA payment configuration
    # All secrets must be stored in the project-root .env file and injected as env vars.
    PAYANYWAY_MNT_ID = os.getenv("PAYANYWAY_MNT_ID")  # merchant account id
    PAYANYWAY_MNT_INTEGRITY_CODE = os.getenv("PAYANYWAY_MNT_INTEGRITY_CODE")  # integrity code
    # Test mode flag (\"1\" or \"0\" as strings for PayAnyWay)
    PAYANYWAY_TEST_MODE = os.getenv("PAYANYWAY_TEST_MODE", "1")
    # Optional parameters – configure if you use non-default values
    PAYANYWAY_MNT_INLINE_FORM = os.getenv("PAYANYWAY_MNT_INLINE_FORM")  # \"1\" to use inline form
    PAYANYWAY_MNT_UNIT_ID = os.getenv("PAYANYWAY_MNT_UNIT_ID")  # specific payment method id
    PAYANYWAY_MNT_SUBSCRIBER_ID = os.getenv("PAYANYWAY_MNT_SUBSCRIBER_ID")  # subscriber id (optional)
    PAYANYWAY_MNT_CMS = os.getenv("PAYANYWAY_MNT_CMS", "TaskListCMS")

    # For SQLite over TCP proxy
    SQLITE_DB_PATH = "/app/db/offcardswood.db"  # Mounted path in container
    # SQLALCHEMY_BINDS = f"sqlite:///{SQLITE_DB_PATH}?mode=ro"  # Read-only mode