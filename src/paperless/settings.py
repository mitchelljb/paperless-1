"""
Django settings for paperless project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e11fl1oa-*ytql8p)(06fbj4ukrlo+n7k&q5+$1md7i+mge=ee'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGIN_URL = '/admin/login'

ALLOWED_HOSTS = []

# Tap paperless.conf if it's available
if os.path.exists("/etc/paperless.conf"):
    load_dotenv("/etc/paperless.conf")



# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "django_extensions",

    "documents.apps.DocumentsConfig",

    "rest_framework",
    "crispy_forms",

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'paperless.urls'

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

WSGI_APPLICATION = 'paperless.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(os.getenv("PAPERLESS_DBLOCATION",os.path.join(BASE_DIR, "..", "data")), "db.sqlite3")
    }
}

if os.getenv("PAPERLESS_DBUSER") and os.getenv("PAPERLESS_DBPASS"):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("PAPERLESS_DBNAME", "paperless"),
        "USER": os.getenv("PAPERLESS_DBUSER"),
        "PASSWORD": os.getenv("PAPERLESS_DBPASS")
    }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "..", "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")

STATIC_URL = '/static/'
MEDIA_URL = "/media/"


# Paperless-specific stuff
# You shouldn't have to edit any of these values.  Rather, you can set these
# values in /etc/paperless.conf instead.
# ----------------------------------------------------------------------------

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "consumer": {
            "class": "documents.loggers.PaperlessLogger",
        }
    },
    "loggers": {
        "documents": {
            "handlers": ["consumer"],
            "level": os.getenv("PAPERLESS_CONSUMER_LOG_LEVEL", "INFO"),
        },
    },
}


# The default language that tesseract will attempt to use when parsing
# documents.  It should be a 3-letter language code consistent with ISO 639.
OCR_LANGUAGE = "eng"

# The amount of threads to use for OCR
OCR_THREADS = os.getenv("PAPERLESS_OCR_THREADS")

# If this is true, any failed attempts to OCR a PDF will result in the PDF
# being indexed anyway, with whatever we could get.  If it's False, the file
# will simply be left in the CONSUMPTION_DIR.
FORGIVING_OCR = bool(os.getenv("PAPERLESS_FORGIVING_OCR", "YES").lower() in ("yes", "y", "1", "t", "true"))

# GNUPG needs a home directory for some reason
GNUPG_HOME = os.getenv("HOME", "/tmp")

# Convert is part of the ImageMagick package
CONVERT_BINARY = os.getenv("PAPERLESS_CONVERT_BINARY")
CONVERT_TMPDIR = os.getenv("PAPERLESS_CONVERT_TMPDIR")
CONVERT_MEMORY_LIMIT = os.getenv("PAPERLESS_CONVERT_MEMORY_LIMIT")
CONVERT_DENSITY = os.getenv("PAPERLESS_CONVERT_DENSITY")

# Unpaper
UNPAPER_BINARY = os.getenv("PAPERLESS_UNPAPER_BINARY", "unpaper")

# This will be created if it doesn't exist
SCRATCH_DIR = os.getenv("PAPERLESS_SCRATCH_DIR", "/tmp/paperless")

# This is where Paperless will look for PDFs to index
CONSUMPTION_DIR = os.getenv("PAPERLESS_CONSUMPTION_DIR")

# If you want to use IMAP mail consumption, populate this with useful values.
# If you leave HOST set to None, we assume you're not going to use this
# feature.
MAIL_CONSUMPTION = {
    "HOST": os.getenv("PAPERLESS_CONSUME_MAIL_HOST"),
    "PORT": os.getenv("PAPERLESS_CONSUME_MAIL_PORT"),
    "USERNAME": os.getenv("PAPERLESS_CONSUME_MAIL_USER"),
    "PASSWORD": os.getenv("PAPERLESS_CONSUME_MAIL_PASS"),
    "USE_SSL": os.getenv("PAPERLESS_CONSUME_MAIL_USE_SSL", "y").lower() == "y",  # If True, use SSL/TLS to connect
    "INBOX": "INBOX"  # The name of the inbox on the server
}

# This is used to encrypt the original documents and decrypt them later when
# you want to download them.  Set it and change the permissions on this file to
# 0600, or set it to `None` and you'll be prompted for the passphrase at
# runtime.  The default looks for an environment variable.
# DON'T FORGET TO SET THIS as leaving it blank may cause some strange things
# with GPG, including an interesting case where it may "encrypt" zero-byte
# files.
PASSPHRASE = os.getenv("PAPERLESS_PASSPHRASE")

# If you intend to use the "API" to push files into the consumer, you'll need
# to provide a shared secret here.  Leaving this as the default will disable
# the API.
SHARED_SECRET = os.getenv("PAPERLESS_SHARED_SECRET", "")

# Trigger a script after every successful document consumption?
PRE_CONSUME_SCRIPT = os.getenv("PAPERLESS_PRE_CONSUME_SCRIPT")
POST_CONSUME_SCRIPT = os.getenv("PAPERLESS_POST_CONSUME_SCRIPT")

#
# TODO: Remove after 0.2
#
# This logic is here to address issue #44, wherein we were using inconsistent
# constant names vs. environment variables.  If you're using Paperless for the
# first time, you can safely ignore everything from here on, so long as you're
# correctly defining the variables as per the documentation.
#


def deprecated(before, after):
    print(
        "\n\n"
        "WARNING: {before} has been renamed to {after}.\n"
        "WARNING: Use of {before} will not work as of version 1.2."
        "\n\n".format(
            before=before,
            after=after
        )
    )

if not CONVERT_BINARY:
    CONVERT_BINARY = "convert"
    if os.getenv("PAPERLESS_CONVERT"):
        deprecated("PAPERLESS_CONVERT", "PAPERLESS_CONVERT_BINARY")
        CONVERT_BINARY = os.getenv("PAPERLESS_CONVERT", CONVERT_BINARY)

if not CONSUMPTION_DIR and os.getenv("PAPERLESS_CONSUME"):
    deprecated("PAPERLESS_CONSUME", "PAPERLESS_CONSUMPTION_DIR")
    CONSUMPTION_DIR = os.getenv("PAPERLESS_CONSUME")

if not SHARED_SECRET and os.getenv("PAPERLESS_SECRET"):
    deprecated("PAPERLESS_SECRET", "PAPERLESS_SHARED_SECRET")
    SHARED_SECRET = os.getenv("PAPERLESS_SECRET", "")
