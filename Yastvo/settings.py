import os
import os.path
import environ 
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'requirements.json')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True))

environ.Env.read_env(BASE_DIR / '.env') 



# False if not in os.environ because of casting above
DEBUG = True



SECRET_KEY = env('SECRET_KEY')
SECURE_HSTS_SECONDS = 600
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ALLOWED_HOSTS = ['*']
#for localhost only
ALLOWED_HOSTS = ["cafe.i-dmytro.pl","test.i-dmytro.pl","127.0.0.1", "152.67.136.138" ]
CSRF_TRUSTED_ORIGINS = ["http://cafe.i-dmytro.pl", "https://cafe.i-dmytro.pl", "http://test.i-dmytro.pl", "https://test.i-dmytro.pl"]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://cafe.i-dmytro.pl",
    "http://cafe.i-dmytro.pl",
    "http://test.i-dmytro.pl",
    "https://test.i-dmytro.pl"
    # Add any other allowed origins here as needed
]

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
    'corsheaders',
    'storages',
    'main',
    'delivery',
    'rosetta',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
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

hostname = os.environ['DBHOST']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ["DBNAME"],
        'USER': os.environ['DBUSER'],
        'PORT':'3306',
        'HOST': hostname,
        'PASSWORD': os.environ['DBPASS']        
    }
}

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
