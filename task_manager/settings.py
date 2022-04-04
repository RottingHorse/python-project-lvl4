"""
Django settings for task_manager project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import types
from pathlib import Path

import dj_database_url
import rollbar
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
CONN_MAX_AGE = 600
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

FIXTURE_DIRS = (os.path.join(BASE_DIR, "fixtures"),)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = (
    "evilmadsquirrel-task-manager.herokuapp.com",
    "localhost",
    "127.0.0.1",
    "webserver",
)

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap4",
    "task_manager.users",
    "task_manager.statuses",
    "task_manager.tasks",
    "task_manager.labels",
    "django_filters",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
)

ROLLBAR = types.MappingProxyType({
    'access_token': os.getenv("ACCESS_TOKEN"),
    'environment': 'development' if DEBUG else 'production',
    'root': BASE_DIR,
})

rollbar.init(**ROLLBAR)

ROOT_URLCONF = "task_manager.urls"

TEMPLATES = (
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
)

WSGI_APPLICATION = "task_manager.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = types.MappingProxyType({
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
})
if not DEBUG:
    DATABASES["default"] = dj_database_url.config(conn_max_age=CONN_MAX_AGE)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = (
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
        "OPTIONS": {
            "min_length": 3,
        },
    },
)

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("en", "English"),
    ("ru", "Russian"),
)

LOCALE_PATHS = (
    BASE_DIR / "locale/",
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
