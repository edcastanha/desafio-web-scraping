from pathlib import Path
import os
from core.helpers.celery_config import *
from kombu import Queue, Exchange

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PG_HOST = os.environ.get('PG_HOST', 'localhost')
PG_USER = os.environ.get('PG_USER', 'postgres')
PG_PASSWORD = os.environ.get('PG_PASSWORD', 'fake123')
PG_DATABASE = os.environ.get('PG_DATABASE', 'simpleDB')
PG_PORT = os.environ.get('PG_PORT', '5432')

RBMQ_HOST = os.environ.get('RBMQ_HOST', 'localhost')
RBMQ_PORT = os.environ.get('RBMQ_PORT', '5672')
RBMQ_USER = os.environ.get('RBMQ_USER', 'guest')
RBMQ_PASS = os.environ.get('RBMQ_PASS', 'guest')
BROKER_URL = os.environ.get('BROKER_URL', 'amqp://guest:guest@localhost:5672')

FTP_PATH  = os.path.join(BASE_DIR, os.environ.get('FTP_PATH', 'ftp'))

EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'MYSECRET', '78cdsvc7sdavb07nvar87ynbdravs7by87yvb7ab09se7vybrsd7vyd9'
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get(
    'MYDEBUG', True
    )

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Libs
    'rest_framework',
    'django_celery_results',
    # Apps
    'core.webScrappingTask.apps.WebscrappingtaskConfig'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://localhost:7000",
    # Adicione outros domínios permitidos conforme necessário
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': PG_DATABASE,
        'USER': PG_USER,
        'PASSWORD': PG_PASSWORD,
        'HOST': PG_HOST,
        'PORT': PG_PORT,
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#CELERY SETTINGS
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_BACKEND = 'django-db://'


CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 1 dia

CELERY_TASK_ROUTES = {
    'core.helpers.tasks.*': {'queue': 'core'},
}
CELERY_QUEUES = (
    Queue('core', Exchange('core'), routing_key='core'),
)

# Inicialização do Celery
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descoberta automática de tarefas em aplicativos Django
app.autodiscover_tasks()