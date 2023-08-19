import os
import os.path
import environ 
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'yastvo-eec660a22e89.json')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECURE_HSTS_SECONDS = 10
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ["https://yastvo.fly.dev", "https://www.yastvo.fly.dev"]
CSRF_COOKIE_DOMAIN = '*.fly.dev'
env = environ.Env(DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / '.env') 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY') 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Google Cloud Storage Configurations
GS_BUCKET_NAME = 'yastvo_bucket'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_CREDENTIALS = credentials
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_FILE_OVERWRITE = False
GS_DEFAULT_ACL = 'publicRead'

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'django.contrib.sites',
    'storages',
    'main',
    'delivery',
    'rosetta',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Yastvo.urls'


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

WSGI_APPLICATION = 'Yastvo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# PostgreSQL

# for production
# DATABASES = {
#     # read os.environ['DATABASE_URL']
#     'default': env.db()  # <-- Updated!
# }

#for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '37485482_yastvo',
        'USER': '37485482_yastvo',
        'PASSWORD': 'Yastvo#2023',
        'HOST': 'serwer2329268.home.pl',
        'PORT': '5432',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'OPTIONS': {
#             'service': 'my_service',
#             'passfile': '.my_pgpass',
#         },
#     }
# }


# Djongo
# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'Yastvo',
#         'ENFORCE_SCHEMA': True,
#         'CLIENT': {
#                 'host': "mongodb+srv://DemetrPI:3PzaX7E1PrgwF5kz@yastvo.to72xso.mongodb.net/?retryWrites=true&w=majority"
#         }
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGE_COOKIE_NAME = 'django_language'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('uk', _('Ukrainian')),
    ('pl', _('Polish'))
)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale/'),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/staticfiles/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'staticfiles')
#  ]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'users'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1

# stripe payment
STRIPE_KEY = ''

TRANSLATABLE_MODEL_MODULES = [
    "menuItems",
]


# This can be a string or callable, and should return a base host that
# will be used when receiving callbacks and notifications from payment
# providers.
#
# Keep in mind that if you use `localhost`, external servers won't be
# able to reach you for webhook notifications.
PAYMENT_HOST = 'localhost:8000'

# Whether to use TLS (HTTPS). If false, will use plain-text HTTP.
# Defaults to ``not settings.DEBUG``.
PAYMENT_USES_SSL = False
