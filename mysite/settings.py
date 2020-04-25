"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gmg#h8(hj6y_%4k+i0f$3x%35d)5tv()!ium0z-xkfp_#6t*nm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']

# Application definition

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'myApp',
  'crispy_forms',
  'django.contrib.humanize',
  'pwa',
  'debug_toolbar',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 管理サイトのログイン機能を通常のログイン機能として使う
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/index01/'
LOGOUT_REDIRECT_URL = '/index01/'

# django-crispy-forms 設定
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# PWAのパス設定
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'myApp/templates/myApp', 'serviceworker.js')

# manifest jasonの設定
PWA_APP_NAME = 'NFA tool'
PWA_APP_DESCRIPTION = "Tool to identify priority commodity for nutrition improvement"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_ORIENTATION = 'any'
PWA_APP_SCOPE = '/'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
  {
    "src": "/static/img/icons/chef72.png",
    "sizes": "72x72",
    "type": "image/png"
  }, {
    "src": "/static/img/icons/chef96.png",
    "sizes": "96x96",
    "type": "image/png"
  }, {
    "src": "/static/img/icons/chef128.png",
    "sizes": "128x128",
    "type": "image/png"
  }, {
    "src": "/static/img/chef144.png",
    "sizes": "144x144",
    "type": "image/png"
  }, {
    "src": "/static/img/icons/chef152.png",
    "sizes": "152x152",
    "type": "image/png"
  }, {
    "src": "/static/img/icons/chef192.png",
    "sizes": "192x192",
    "type": "image/png"
  }, {
    "src": "/static/img/icons/chef384.png",
    "sizes": "384x384",
    "type": "image/png"
  }, {
    "src": "/static/img/icons/chef512.png",
    "sizes": "512x512",
    "type": "image/png"
  }
]

PWA_APP_SPLASH_SCREEN = [
  {
    'src': '/static/img/icons/mother and child 640.png',
    'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
  }
]
PWA_APP_LANG = 'en-US'

# DataFlair #Logging Information
LOGGING = {
  'version': 1,
  # Version of logging
  'disable_existing_loggers': False,
  # disable logging
  # --------------Formatter-----------------------
  'formatters': {
    'detail': {
      'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
      'style': '{',
    },
    'medium': {
      'format': '{levelname} [{filename}-{funcName}-{lineno}] {message}',
      'style': '{',
    },
    'simple': {
      'format': '{levelname} {message}',
      'style': '{',
    },
  },
  # Handlers #############################################################
  'handlers': {
    'file': {
      'level': 'DEBUG',
      'class': 'logging.FileHandler',
      'filename': 'shunichi-debug.log',
      'formatter': 'medium'
    },
    ##------------------------------------------------------
    'console': {
      'level': 'INFO',
      'class': 'logging.StreamHandler',
      'formatter': 'medium'
    },
  },
  # Loggers ####################################################################
  'loggers': {
    'myApp': {
      'handlers': ['console'],
      'level': 'INFO',
      'propagate': True,
#      'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG')
    },
  },
}

# # For debugging
# if DEBUG:
#   # will output to your console
#   logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s %(message)s',
#   )
# else:
#   # will output to logging file
#   logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s %(message)s',
#     filename='/my_log_file.log',
#     filemode='a'
#   )

# for messaging
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
  messages.DEBUG: 'alert-info',
  messages.INFO: 'alert-info',
  messages.SUCCESS: 'alert-success',
  messages.WARNING: 'alert-warning',
  messages.ERROR: 'alert-danger',
}
