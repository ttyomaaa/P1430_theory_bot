from dotenv import load_dotenv
from aiogram import Bot
import os

load_dotenv()

# database
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

ASYNC_DRIVER_NAME = 'postgresql+asyncpg'
PSYCOPG_DRIVER_NAME = 'postgresql+psycopg2'

# paths

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bot = Bot(token='', parse_mode="html")
