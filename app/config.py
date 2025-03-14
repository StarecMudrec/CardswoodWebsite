from dotenv import load_dotenv
import os
import hashlib
import os

JWT_SECRET_KEY = "COOL"
BOT_TOKEN_HASH = hashlib.sha256("7505659847:AAF3AoBU0HFInjsPPOqz4KaPmX3M15l9f1U".encode())
COOKIE_NAME = 'auth-token'