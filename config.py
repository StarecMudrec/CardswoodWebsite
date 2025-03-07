from dotenv import load_dotenv
import os

load_dotenv()

SERVER_ADDRESS = os.getenv('SERVER_ADDRESS', '0.0.0.0')
SERVER_PORT = os.getenv('SERVER_PORT', 8080)
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'prod')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
POSTGRES_CONN = "postgresql://{}:{}@{}:{}/{}".format(POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE)
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
ANTIFRAUD_ADDRESS = os.getenv('ANTIFRAUD_ADDRESS')
RANDOM_SECRET = os.getenv('RANDOM_SECRET', 'kys')


APP_DEBUG = bool(os.getenv('APP_DEBUG'))