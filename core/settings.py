from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True") == "True"

if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ── Content Security Policy ─────────────────────────────────────────────────
CSP_DIRECTIVES = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
    "style-src": [
        "'self'",
        "'unsafe-inline'",
        "https://fonts.googleapis.com",
        "https://cdnjs.cloudflare.com",
    ],
    "font-src": [
        "'self'",
        "https://fonts.gstatic.com",
        "https://cdnjs.cloudflare.com",
    ],
    "img-src": ["'self'", "data:"],
    "connect-src": ["'self'"],
    "object-src": ["'none'"],
    "base-uri": ["'self'"],
    "form-action": ["'self'"],
    "frame-ancestors": ["'none'"],
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = ["*"]
_origins = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = []
for _o in (o.strip() for o in _origins.split(",") if o.strip()):
    if _o.startswith(("http://", "https://")):
        CSRF_TRUSTED_ORIGINS.append(_o)
    else:
        # Sem esquema: adiciona http e https para não bloquear nenhum dos dois
        CSRF_TRUSTED_ORIGINS.append(f"http://{_o}")
        CSRF_TRUSTED_ORIGINS.append(f"https://{_o}")

# Application definition

INSTALLED_APPS = [
    "core.mongo_apps.MongoContentTypesConfig",
    "django.contrib.staticfiles",
    "agenda",
    "financeiro",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.ContentSecurityPolicyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.MobileDetectionMiddleware",
]

# Login sistema desabilitado por enquanto
CSRF_ENABLED = False


ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_mongodb_backend",
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": int(os.getenv("DB_PORT", 27017)),
        "CLIENT": {"tlsAllowInvalidCertificates": True},
    }
}



# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Additional locations of static files
STATICFILES_DIRS = [
    BASE_DIR / "agenda" / "static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Se você não rodar o comando 'python manage.py collectstatic',
# o Whitenoise precisa buscar os estáticos diretamente nos STATICFILES_DIRS.
# Isso evita problemas com o arquivo CSS não sendo encontrado com o Gunicorn.
WHITENOISE_USE_FINDERS = True

# Tempo em segundos que o navegador deve guardar os arquivos estáticos
WHITENOISE_MAX_AGE = 600  # 10 minutos

# Default primary key field type
# https://docs.djangoproject.com/en/6.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"



# ── E-mail (Hostinger SMTP) ─────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.hostinger.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_FROM", EMAIL_HOST_USER)
