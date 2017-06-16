from __future__ import absolute_import, unicode_literals
"""
Django settings for suqihan project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAIN_APP = "suqihan"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mju1l7k^wkh-f)16*fenp@6hq%v($%m=ng5miqbhjn-s-(=w3r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','localhost', '127.0.0.1','0.0.0.0']

ADMINS = (
    ('suxuekun','suxuekundev@gmail.com'),
)

MANAGERS = (
    ('suxuekun','suxuekundev@gmail.com'),
)

EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'suxuekundev@gmail.com'
EMAIL_HOST_PASSWORD = 'demo'
# EMAIL_HOST = 'smtp.office365.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
DEFAULT_TO_EMAIL = EMAIL_HOST_USER

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    MAIN_APP
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = MAIN_APP+'.urls'

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(module)s|%(process)d|%(thread)d|%(message)s'
        },
        'simple': {
            'format': '%(levelname)s|%(message)s'
        },
        'simple-time':{
            'format': '%(levelname)s|%(asctime)s|%(message)s'
        }
    },
    'handlers': {
        'file_debug': {
            'level': 'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*10,
            'filename': BASE_DIR+'/logs/debug.log',
            'formatter': 'simple-time'
        },'file_info': {
            'level': 'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*10,
            'filename': BASE_DIR+'/logs/info.log',
            'formatter': 'simple-time'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file_debug'],
            'level': 'DEBUG',
            'propagate': True,
        },'app':{
            'handlers': ['file_info'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+"/templates",BASE_DIR+"/"+MAIN_APP+'/templates'],
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

WSGI_APPLICATION = MAIN_APP+'.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'suqihan',
        'USER': 'root',
        'PASSWORD': 'sillyboy',
        'HOST': '127.0.0.1',
        'PORT': '8889',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 60*60
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        MAIN_APP+'.base.permission.IsAuthenticatedReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
                                'rest_framework.filters.OrderingFilter',
                                'rest_framework.filters.SearchFilter',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = BASE_DIR+'/static/'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = '/media/'
TRASH_ROOT = MEDIA_ROOT + "trash/"
TEMP_ROOT = MEDIA_ROOT + "temp/"
TEMPLATE_URL = '/template/'
TEMPLATE_ROOT = BASE_DIR + '/'+MAIN_APP+'/templates/'

TRANSLATE_ROOT = STATIC_ROOT + 'i18n/'

FILE_UPLOAD_MAX_MEMORY_SIZE=1024*1024*10

if DEBUG:
    print 'base',BASE_DIR
    print 'static',STATIC_ROOT
    print 'media',MEDIA_ROOT
    print 'trash',TRASH_ROOT
    print 'temp',TEMP_ROOT
    print 'template',TEMPLATE_ROOT
    print 'translate',TRANSLATE_ROOT
    print 'upload_max',FILE_UPLOAD_MAX_MEMORY_SIZE
    print 'LANGUAGE_CODE',LANGUAGE_CODE
    print 'TIME_ZONE',TIME_ZONE
    print 'SESSION_COOKIE_AGE',SESSION_COOKIE_AGE
    for key,items in DATABASES.iteritems():
        print 'database_'+key,items['NAME']
    
    