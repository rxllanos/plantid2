
from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-^f36+yx*53zu(#c78vzjob+%&t^2mqij4tmzu9inr^p8szodct'
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1','lasmirlas.azurewebsites.net']

CSRF_TRUSTED_ORIGINS = [
    'https://lasmirlas.azurewebsites.net',
    'http://127.0.0.1:8000/'
]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
    'https://lasmirlas.azurewebsites.net'
]

INSTALLED_APPS = [
    'planta.apps.PlantaConfig',
    'crispy_forms',
    'corsheaders',
    'crispy_bootstrap5',
    'storages',    
    'django.contrib.admin',
    'django.contrib.postgres',
    'accounts',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'accounts.CustomUser'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
ROOT_URLCONF = 'plantas.urls'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
TEMPLATES_DIR = os.path.join(BASE_DIR)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'plantas','templates','plantas')],
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

# WSGI_APPLICATION = 'plantas.wsgi.application'

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config('PGDATABASE'),
        "USER": config('PGUSER'),
        "PASSWORD": config('PGPASSWORD'),
        "HOST": config('PGHOST'),
        "PORT": config('PGPORT'),
        "OPTION":{"sslmode":'require'},
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

STORAGES = {
    "default": {"BACKEND": "plantas.azure_storage.AzureMediaStorage"},
    "staticfiles": {"BACKEND": "plantas.azure_storage.AzureStaticStorage"},
}

AZURE_ACCOUNT_NAME = config('AZURE_ACCOUNT_NAME')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/static-agriculture/'
# STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/media-agriculture/'
# MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'plantas','static'),
]



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

