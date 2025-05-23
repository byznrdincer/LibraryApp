import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# GÜVENLİK
SECRET_KEY = 'E1Om-ZK2xdN-kge_XbopKZJvbROYqb7xp8rHy2D2Db9vTjYr5u-CEURnbpt30uWhHV0'
DEBUG = False
ALLOWED_HOSTS = ['libraryapp-0eir.onrender.com']

# UYGULAMALAR
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library_core',
    'django_celery_beat',
    'django_extensions',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLS ve TEMPLATES
ROOT_URLCONF = 'LibraryApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'LibraryApp.wsgi.application'

# ✅ MySQL AYARI (Render ortamı için localhost DEĞİL!)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library_app',
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': 'mysql-db',  # Render'da MySQL servisine verilen isim
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# PAROLA VALIDATORLERİ
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# DİL ve ZAMAN
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ STATİK DOSYA AYARI (Render için WhiteNoise)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ GMAIL SMTP AYARI
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'beyzanurdincer502@gmail.com'
EMAIL_HOST_PASSWORD = 'Gmail-uygulama-şifren-buraya'  # Gerçek şifre değil, uygulama şifresi

# ✅ GİRİŞ YÖNLENDİRME
LOGIN_REDIRECT_URL = '/afterlogin'

# ✅ CELERY (Redis Render servisine göre ayarlandı)
CELERY_BROKER_URL = 'redis://default:password@redis:6379/0'  # 'redis' burada Render servis adı
CELERY_RESULT_BACKEND = 'redis://default:password@redis:6379/0'
CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
