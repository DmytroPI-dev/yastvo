import os
from pathlib import Path
import environ
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Reading .env file
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False) # Default to False for production
)
environ.Env.read_env(BASE_DIR / '.env')

# --- Core Settings ---
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

# --- Security Settings ---
ALLOWED_HOSTS = ["cafe.i-dmytro.org"]
CSRF_TRUSTED_origins = ["https://cafe.i-dmytro.org"]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://cafe.i-dmytro.org",
]
SECURE_HSTS_SECONDS = 600
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# --- Application Definition ---
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
    # 'storages', # Removed as we are using local storage
    'main',
    'delivery',
    'rosetta',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware', # Removed as Nginx handles static files
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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


# --- Database ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ["DBNAME"],
        'USER': os.environ['DBUSER'],
        'PORT':'3306',
        'HOST': os.environ['DBHOST'],
        'PASSWORD': os.environ['DBPASS']
    }
}


# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internationalization ---
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('uk', _('Ukrainian')),
    ('pl', _('Polish'))
)
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale/'),)
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# --- Static and Media Files (Local Configuration) ---
# The URL prefix for static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
# The absolute path to the directory where `collectstatic` will collect static files.
STATIC_ROOT = BASE_DIR / 'static'

# The URL that handles media files served from MEDIA_ROOT.
MEDIA_URL = '/media/'
# The absolute path to the directory that will hold user-uploaded files.
MEDIA_ROOT = BASE_DIR / 'media'


# --- Django Defaults ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'users'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1
