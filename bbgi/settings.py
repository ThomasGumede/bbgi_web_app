from pathlib import Path
import os, re
# from bbgi.celery_settings import *
from bbgi.logging_settings import LOGGING
from decouple import config, Csv
from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_EXTENDED = True
CELERY_worker_state_db = True
CELERY_result_persistent = True
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Africa/Johannesburg'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # Optional, for timeout adjustments
CELERY_TASK_IGNORE_RESULT = True
CELERY_ACKS_LATE = True  # Ensures tasks are acknowledged after execution
CELERY_RETRY_POLICY = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.5,
}

CELERY_BEAT_SCHEDULE = {
    
    # 'send-email-update': {
    #     'task': 'home.tasks.send_update_email',
    #     'schedule': crontab(hour=9, minute=0),  # Run the task 23 hours
    # },
    'close-expired-events': {
        'task': 'events.tasks.check_2_events_status',
        'schedule': crontab(hour=9, minute=0)
    },
    'close-expired-campaigns': {
        'task': 'campaigns.tasks.check_2_campaigns_status',
        'schedule': crontab(hour=9, minute=0)
    },
}

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET', 'django-insecure-3y8rwrn(uibq1y74d_(taob6lm1-8fe)wp6=99iqbu9z#b814+')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

RECAPTCHA_ENTERPRISE_PROJECT_ID = config('RECAPTCHA_ENTERPRISE_PROJECT_ID')
RECAPTCHA_ENTERPRISE_SITE_KEY = config('RECAPTCHA_ENTERPRISE_SITE_KEY')
GOOGLE_APPLICATION_CREDENTIALS = '/path/to/your/service-account-key.json'
#  Custom User model
AUTH_USER_MODEL = 'accounts.Account'
AUTHENTICATION_BACKENDS = ['accounts.utilities.backends.EmailBackend']
LOGIN_URL = 'accounts:login'
ADMINS = [('admin@bbgi.co.za'),( 'support@bbgi.co.za'), ('gumedethomas12@gmail.com') ]
MANAGERS = [('admin@bbgi.co.za'), ('support@bbgi.co.za'), ('gumedethomas12@gmail.com') ]

# Security
CSRF_TRUSTED_ORIGINS = ['https://127.0.0.1', 'https://localhost', 'https://bbgi.co.za', 'https://www.bbgi.co.za']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ['security.W019']
TEST_MODE = config('YOCO_TEST_MODE')

if TEST_MODE == 'yes':
    YOCO_WEBHOOK_KEY = config('YOCO_TEST_WEBHOOK_KEY')
    YOCO_API_KEY = config('YOCO_TEST_API_KEY')
else:
    YOCO_WEBHOOK_KEY = config('YOCO_LIVE_WEBHOOK_KEY')
    YOCO_API_KEY = config('YOCO_LIVE_API_KEY')


# YOCO
if DEBUG:
    
    ALLOWED_HOSTS=['*']

else:
    
    

    # SSL SETTINGS
    
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Allowed Hosts
    ALLOWED_HOSTS = ['bbgi.co.za', 'www.bbgi.co.za', 'localhost', '102.219.85.210', '0.0.0.0']


# Files
TICKETS_PDF_DIR = os.path.join(BASE_DIR, 'media/tickets/pdf')
TICKETS_BARCODE_DIR = os.path.join(BASE_DIR, 'media/tickets/barcodes')
TICKETS_QRCODE_DIR = os.path.join(BASE_DIR, 'media/tickets/qrcodes')

if not os.path.exists(TICKETS_PDF_DIR):
    os.makedirs(TICKETS_PDF_DIR)

if not os.path.exists(TICKETS_BARCODE_DIR):
    os.makedirs(TICKETS_BARCODE_DIR)

if not os.path.exists(TICKETS_QRCODE_DIR):
    os.makedirs(TICKETS_QRCODE_DIR)




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    
    'accounts.apps.AccountsConfig',
    'bbgi_home',
    'listings',
    'campaigns.apps.CampaignsConfig',
    'events.apps.EventsConfig',
    "markets",
    'payments.apps.PaymentsConfig',
    'coupons',
    
    'tailwind',
    'theme',
    'tinymce',
    'django_celery_beat',
    'django_celery_results',
    'fontawesomefree',
    # "django.contrib.sites",
    # 'django.contrib.sitemaps',
]

GOOGLE_ANALYTICS_MEASUREMENT_ID = config('GOOGLE_G')

TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = "/usr/bin/npm"
INTERNAL_IPS = [
    "127.0.0.1", '0.0.0.0'
]
PASSWORD_RESET_TIMEOUT = 14400

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5MB

TINYMCE_DEFAULT_CONFIG = {
    'content_style': '* { margin: 0 !important; padding: 0 !important; }',
    'theme_advanced_fonts': 'DM Sans=dm-sans,Arial=arial,helvetica,sans-serif',
    'height': "400px",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    # 'selector': 'textarea',
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks fullscreen insertdatetime media table paste help",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | a11ycheck ltr rtl | showcomments addcomment",
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bbgi.urls'

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
                'bbgi_home.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'bbgi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEBUG:

    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': "bbgidb",
                'USER': config("DB_USER"),
                'PASSWORD': config("DB_PASSWORD"),
                'HOST': config("DB_HOST",'localhost'),
                'PORT': '',
            }
    }
else:

    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': "bbgidb",
                'USER': config("DB_USER"),
                'PASSWORD': config("DB_PASSWORD"),
                'HOST': config("DB_HOST",'localhost'),
                'PORT': '',
            }
        }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_TZ = True


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

if DEBUG:

    STATIC_URL = 'static/'
    STATICFILES_DIRS = [
        BASE_DIR / 'static'
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
else:
    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.siyazalana.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@siyazalana.org'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'noreply@bbgi.co.za'
