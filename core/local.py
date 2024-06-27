import os
from pathlib import Path
from dotenv import load_dotenv

# .env faylni o'qish
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = ['*']
DEBUG = True


CORS_ALLOWED_ORIGINS = [
    "http://172.16.15.15",
    "http://localhost:8000",
    'http://0.0.0.0',
    'http://127.0.0.1',
    'http://172.16.13.168',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv("DB_NAME"),
#         'USER': os.getenv("DB_USER"),
#         'PASSWORD': os.getenv("DB_PASS"),
#         'HOST': os.getenv("DB_HOST"),
#         'PORT': os.getenv("DB_PORT"),
#     }
# }

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# Hemis OAuth2 konfiguratsiyasi
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI_LOCAL")
AUTHORIZE_URL = os.getenv("AUTHORIZE_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
RESOURCE_OWNER_URL = os.getenv("RESOURCE_OWNER_URL")
