"""
Django settings for myshop project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '97vqo*t)m)h_3pjjw4(=9m&kc*-_a*30icly_ifg$80jeg_cbz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'shop',
    'cart',
    'orders',
    'payment',
    'coupons',

    # third party apps
    'paypal.standard.ipn',
    'rosetta',
    'parler',
    'localflavor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    # для intenationalization
    'django.middleware.locale.LocaleMiddleware',
    # -----------------------
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'myshop.urls'

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
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
# языковые настройки

# стандартный язык
LANGUAGE_CODE = 'en'

from django.utils.translation import gettext_lazy as _

# языки которые будут использоваться для перевода
LANGUAGES = (
    ('en', _('English')),
    ('uk', _('Ukrainian')),
)

# указывается, где должны будут находится файлы с переводами
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CART_SESSION_ID = 'cart'

# для вывода отправленых писем в консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# django-paypal options
# нельзя использовать настоящий email адрес при
# имитации оплаты с помощью sandbox paypal
# иниче у процеса оплаты будет висеть статус pending 
# и заказ не будет оплачен
PAYPAL_RECEIVER_EMAIL = 'phonxis-facilitator@gmail.com'
PAYPAL_TEST = True

# django-parler
PARLER_LANGUAGES = {
    None: (
        {'code': 'en',},
        {'code': 'uk',},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False,
    }
}

# redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1
