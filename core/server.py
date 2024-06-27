import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = ['*']
DEBUG = os.getenv("DEBUG")
# DEBUG = False
#
CSRF_TRUSTED_ORIGINS = [
    'https://arm.namspi.uz',
    'http://172.16.13.168',
    'http://localhost',
    'http://0.0.0.0',
    'http://127.0.0.1',
    'https://namspi.uz'
]
# CSRF_TRUSTED_ORIGINS = ['t3-production-7759.up.railway.app']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASS"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

#static
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTHORIZE_URL = os.getenv("AUTHORIZE_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
RESOURCE_OWNER_URL = os.getenv("RESOURCE_OWNER_URL")


