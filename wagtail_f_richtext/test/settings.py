"""
Django settings for temp project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import os

from wagtail import VERSION as WAGTAIL_VERSION

# Build paths inside the project like this: os.path.join(PROJECT_DIR, ...)
TESTAPP_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "development-only-secret-key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

if WAGTAIL_VERSION >= (3, 0):
    WAGTAIL = "wagtail"
else:
    WAGTAIL = "wagtail.core"

INSTALLED_APPS = [
    "wagtail_f_richtext",
    "wagtail_f_richtext.test",
    "wagtail.contrib.redirects",
    "wagtail.users",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail.sites",
    WAGTAIL,
    "taggit",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "wagtail_f_richtext.test.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


# Using DatabaseCache to make sure that the cache is cleared between tests.
# This prevents false-positives in some wagtail core tests where we are
# changing the 'wagtail_root_paths' key which may cause future tests to fail.
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.db.DatabaseCache",
#         "LOCATION": "cache",
#     }
# }


# don't use the intentionally slow default password hasher
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(TESTAPP_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(TESTAPP_DIR, "static"),
]

# STATIC_ROOT = os.path.join(TESTAPP_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(TESTAPP_DIR, "media")
MEDIA_URL = "/media/"


# Wagtail settings

WAGTAIL_SITE_NAME = "Wagtail F Richtext test site"

WAGTAILADMIN_BASE_URL = "http://localhost:8000/admin"

CSS_CDN_URL = "https://unpkg.com/codyhouse-framework/main/assets/css/style.min.css"

# FRAMEWORK STYLES
F_RICHTEXT_FRAMEWORK_CONFIG = {
    "classes": {
        "h1": "heading-1",
        "h2": "heading-2",
        "ul": "list list--ul",
        "ol": "list list--ol",
        "a": "color-contrast-higher",
        "b": "font-bold",
        "i": "font-italic",
    },
    "wrapper_classes": [
        "text-component",
    ],
    "alignment_classes": {
        "richtext-image left": "f-richtext-image f-richtext-image--left",
        "richtext-image right": "f-richtext-image f-richtext-image--right",
        "richtext-image full-width": "margin: 1em 0; width: 100%; height: auto;",
    },
    "remove_empty_tags": [
        "p",
    ],
    "append_clearfix": True,
}

# INTERNAL STYLES
F_RICHTEXT_INLINE_CONFIG = {
    "styles": {
        "h1": "margin-bottom: 1em;",
        "h2": "margin-bottom: 1em;",
        "h3": "margin-bottom: 1em;",
        "h4": "margin-bottom: 1em;",
        "h5": "margin-bottom: 1em;",
        "h6": "margin-bottom: 1em;",
        "p": "margin-bottom: 1em;",
        "ul": "float: none; clear: both; list-style: disc; margin-left: 2em; margin-bottom: 1em;",
        "ol": "float: none; clear: both; list-style: decimal; margin-left: 2em; margin-bottom: 1em;",
        "code": "font-family: monospace; background-color: #f5f5f5; padding: 0.25rem 0.5rem;",
        "sub": "vertical-align: sub; font-size: smaller;",
        "sup": "vertical-align: super; font-size: smaller;",
        "div": "float: none; clear: both;",
        "iframe": "max-width: 100%; width: 720px; height: 400px; margin-top: 1em; margin-bottom: 1em;",
        "b": "font-weight: bold;",
        "i": "font-style: italic;",
    },
    "wrapper_styles": [
        "overflow:hidden;",
    ],
    "alignment_styles": {
        "richtext-image left": "float: left; margin-right: 1rem; margin-left: 0; margin-bottom: 1rem; height: auto;",
        "richtext-image right": "float: right; margin-left: 1rem; margin-right: 0; margin-bottom: 1rem; height: auto;",
        "richtext-image full-width": "margin: 1em 0; width: 100%; height: auto;",
    },
    "remove_empty_tags": [
        "p",
    ],
    "append_clearfix": True,
}

try:
    from .gitpod_settings import *  # noqa
except ImportError:
    pass
