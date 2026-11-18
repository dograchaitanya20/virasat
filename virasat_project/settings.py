"""
Django settings for Virasat (विरासत) project.
"""

from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, 'virasat-secret-key-heritage-showcase-2026-production-ready'),
    ALLOWED_HOSTS=(list, ['*']),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
)

environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', 'testserver', '*'])
if 'testserver' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('testserver')

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
_render_url = os.environ.get('RENDER_EXTERNAL_URL')  # set automatically by Render
if _render_url:
    CSRF_TRUSTED_ORIGINS.append(_render_url)
CSRF_TRUSTED_ORIGINS += env.list('CSRF_TRUSTED_ORIGINS', default=[])

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Application definition
INSTALLED_APPS = [
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third Party
    'rest_framework',

    # Virasat Apps
    'apps.core.apps.CoreConfig',
    'apps.states.apps.StatesConfig',
    'apps.heritage.apps.HeritageConfig',
    'apps.festivals.apps.FestivalsConfig',
    'apps.arts.apps.ArtsConfig',
    'apps.cuisine.apps.CuisineConfig',
    'apps.stories.apps.StoriesConfig',
    'apps.quiz.apps.QuizConfig',
    'apps.accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'virasat_project.urls'

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
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'apps.core.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'virasat_project.wsgi.application'

DATABASES = {
    'default': env.db()
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('hi', 'हिन्दी (Hindi)'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static and Media Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
