import os

from dotenv import load_dotenv

load_dotenv('.env.dist')

qiwi_public_key = os.getenv("QIWI_KEY")
vk_api_service_key = os.getenv("VK_API_SERVICE_KEY")
qiwi_number = os.getenv("QIWI_NUMBER")
qiwi_token = os.getenv("QIWI_TOKEN")

BOT_TOKEN = os.getenv("BOT_TOKEN")
admins = [os.getenv("ADMIN_ID")]

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME")

