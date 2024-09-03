"""."""

import os

from dotenv import load_dotenv

load_dotenv(encoding='latin-1')

DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

load_dotenv('.test.env', encoding='latin-1')

DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')
DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')

SECRET_KEY = os.getenv('SECRET_KEY')


SMTP_SERVER = str(os.environ.get('SMTP_SERVER'))
SMTP_PORT = int(os.environ.get('SMTP_PORT'))
SMTP_USER = str(os.environ.get('SMTP_USER'))
SMTP_PASSWORD = str(os.environ.get('SMTP_PASSWORD'))
