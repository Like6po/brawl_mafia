import os

from dotenv import load_dotenv

load_dotenv('.env.dist')

BOT_TOKEN = os.getenv("BOT_TOKEN")
admins = [os.getenv("ADMIN_ID")]

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME")

