import os

from dotenv import load_dotenv

load_dotenv()

USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE_NAME')
