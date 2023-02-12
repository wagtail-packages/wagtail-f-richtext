import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = "development-only-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "tests.testapp",
    "wagtail_f_richtext",
    "wagtail.contrib.redirects",
    "wagtail.users",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail.sites",
    "wagtail",
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

ROOT_URLCONF = "tests.urls"

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

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

if os.getenv("DATABASE") == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "postgres"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

if os.getenv("DATABASE") == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "mysql"),
            "USER": os.getenv("DB_USER", "root"),
            "PASSWORD": os.getenv("DB_PASSWORD", "mysql"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "3306"),
        }
    }

USE_TZ = True

STATICFILES_FINDERS = [
    # "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(PROJECT_DIR, "static")
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")
MEDIA_URL = "/media/"

WAGTAIL_SITE_NAME = "Wagtail F Richtext test app"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

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
