from pathlib import Path
import os, re
# from bbgi.celery_settings import *
from bbgi.logging_settings import LOGGING
from decouple import config, Csv
from celery.schedules import crontab
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

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
    "unfold",
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    
    'accounts.apps.AccountsConfig',
    'bbgi_home.apps.BbgiHomeConfig',
    'listings.apps.ListingsConfig',
    'campaigns.apps.CampaignsConfig',
    'events.apps.EventsConfig',
    "markets.apps.MarketsConfig",
    'payments.apps.PaymentsConfig',
    'coupons.apps.CouponsConfig',
    'bbgistore.apps.BbgistoreConfig',
    
    'tailwind',
    'theme',
    'tinymce',
    'django_celery_beat',
    'django_celery_results',
    'fontawesomefree',
    'taggit',
    'taggit_autosuggest',
    # "django.contrib.sites",
    # 'django.contrib.sitemaps',
]

GOOGLE_ANALYTICS_MEASUREMENT_ID = config('GOOGLE_G')

TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
# NPM_BIN_PATH = "/usr/bin/npm"
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
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
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

USE_GMAIL = config('USE_GMAIL', default=False, cast=bool)

if USE_GMAIL:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = 'bbgiptyltd@gmail.com'
    EMAIL_HOST_PASSWORD = config("GMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = 'BBGI (Pty) Ltd <bbgiptyltd@gmail.com>'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'mail.bbgi.co.za'
    EMAIL_PORT = 465
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
    EMAIL_HOST_USER = 'noreply@bbgi.co.za'
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = 'BBGI <noreply@bbgi.co.za>'

UNFOLD = {

    "SITE_TITLE": "BBGI Administration",

    "SITE_HEADER": "BBGI",

    "SITE_SYMBOL": "dashboard",

    "SHOW_HISTORY": True,
    "SITE_URL": "/",

    "SHOW_VIEW_ON_SITE": True,
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": _("My site"),
            "link": "https://example.com",
            "attrs": {
                "target": "_blank",
            },
        },
        {
            "icon": "diamond",
            "title": _("My site"),
            "link": reverse_lazy("admin:index"),
        },
    ],
    "SITE_ICON": {
        "light": lambda request: static("imgs/android-chrome-512x512.png"),  # light mode
        "dark": lambda request: static("imgs/android-chrome-512x512.png"),  # dark mode
    },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    "SITE_LOGO": {
        "light": lambda request: static("images/logo.png"),  # light mode
        "dark": lambda request: static("images/logo-light.png"),  # dark mode
    },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("imgs/favicon-32x32.png"),
        },
    ],
    
    "COLORS": {

        "primary": {
            "50": "250 247 234",
            "100": "244 238 203",
            "200": "236 225 159",
            "300": "226 210 116",
            "400": "217 196 92",
            "500": "209 181 75",   # Your Gold
            "600": "184 159 47",
            "700": "156 135 40",
            "800": "126 109 32",
            "900": "94 82 24",
        },

    },
    "STYLES": [

        lambda request: static("admin/css/bbgi-admin.css"),

    ],
    "ENVIRONMENT": "Dev", # environment name in header
    "ENVIRONMENT_TITLE_PREFIX": "Dev", # environment name prefix in title tag
    "THEME": "dark",
}


