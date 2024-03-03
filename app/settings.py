import os

from dotenv import load_dotenv


load_dotenv()


DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']

JWT_TOKEN_LIFETIME_IN_MINUTES = int(os.environ['JWT_TOKEN_LIFETIME_IN_MINUTES'])
