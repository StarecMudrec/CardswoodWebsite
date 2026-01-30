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

    # PostgreSQL: задаётся через env (на сервере должен совпадать пароль с контейнером db)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql+psycopg2://postgres:postgres@db:5432/cards"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")


    # For SQLite over TCP proxy
    SQLITE_DB_PATH = "/app/db/offcardswood.db"  # Mounted path in container
    # SQLALCHEMY_BINDS = f"sqlite:///{SQLITE_DB_PATH}?mode=ro"  # Read-only mode

    # PayAnyWay payment integration (from env; optional for local dev)
    PAYANYWAY_MNT_ID = os.getenv("PAYANYWAY_MNT_ID", "")
    # Код проверки целостности данных — из ЛК PayAnyWay (подпись формы и callback)
    PAYANYWAY_SIGNATURE_KEY = os.getenv("PAYANYWAY_MNT_INTEGRITY_CODE") or os.getenv("PAYANYWAY_SIGNATURE_KEY", "")
    PAYANYWAY_TEST_MODE = os.getenv("PAYANYWAY_TEST_MODE", "").strip().lower() in ("1", "true", "yes")
    # Формула подписи (MONETA.Assistant.ru.pdf, cmsspecification): v1=ID+TRANSACTION_ID+AMOUNT+CURRENCY+key; v2=ID+AMOUNT+TRANSACTION_ID+key; v3=как v2, сумма целым; v4=ID+TRANSACTION_ID+key (без суммы). Для assistant.htm обычно v1 или v2.
    PAYANYWAY_SIGNATURE_VERSION = os.getenv("PAYANYWAY_SIGNATURE_VERSION", "v1").strip().lower()
    PAYANYWAY_PAYMENT_URL = os.getenv(
        "PAYANYWAY_PAYMENT_URL",
        "https://payanyway.ru/assistant.htm"
    )
    FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "https://cardswood.ru")
    _base = os.getenv("FRONTEND_BASE_URL", "https://cardswood.ru")
    PAYANYWAY_SUCCESS_URL = os.getenv("PAYANYWAY_SUCCESS_URL", f"{_base}/shop/success")
    PAYANYWAY_FAIL_URL = os.getenv("PAYANYWAY_FAIL_URL", f"{_base}/shop/fail")