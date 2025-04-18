"""
Django settings for personalWebpage project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import psycopg2
from utils.config import REDIS_CONFIG, POSTGRES_CONFIG, DJANGO_SECRET_KEY

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'www.jkirstein.dk', 'jkirstein.dk', '192.168.1.116', 'localhost','django']

# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontpage',
    'literature',
    'personalWebpage',
    'about',
    'foundationResponse',
    'rest_framework',
    'airflow',
    'corsheaders',
    'system_metrics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "https://jkirstein.dk",  # your production domain
    "http://localhost",      # local development domain
    "http://localhost:8000", # local development with Django running on port 8000
    "ws://localhost:8001",
]

ROOT_URLCONF = 'personalWebpage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'personalWebpage.wsgi.application'  # For traditional HTTP requests
ASGI_APPLICATION = 'personalWebpage.asgi.application'  # For WebSockets and async features


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_CONFIG["dbname"],
        'USER': POSTGRES_CONFIG["user"],
        'PASSWORD': POSTGRES_CONFIG["password"],
        'HOST': POSTGRES_CONFIG["host"],
        'PORT': POSTGRES_CONFIG["port"],
    }
}


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_CONFIG["host"], REDIS_CONFIG["port"])],
        },
    },
}



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "static"),  # Use relative path
#]

STATICFILES_DIRS = [
    "/personalWebpage/django/static",  # Use relative path
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Replace 'media' with your folder name if different


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login_user/'
LOGIN_REDIRECT_URL = '/logged_in/'
LOGOUT_REDIRECT_URL = '/login_user/'


CSRF_TRUSTED_ORIGINS = [
    "https://jkirstein.dk",
    "https://www.jkirstein.dk",
    "http://localhost:8000",  # Django (HTTP)
    "http://127.0.0.1:8000",
    "ws://localhost:8000",  # WebSocket (WS)
    "ws://127.0.0.1:8000",
    "http://localhost", 
    "http://127.0.0.1"
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
