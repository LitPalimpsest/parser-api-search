import os
from settings import *
from YamJam import yamjam

PROJECT_PATH = os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

CFG = yamjam(os.path.join(PROJECT_PATH, 'etc/yamjam/config.yaml'))['litlong']

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = CFG['secret-key']

DATABASES = {
    'default': {
        'ENGINE': CFG['env']['local']['database']['engine'],
        'NAME': CFG['env']['local']['database']['name'],
        'USER': CFG['env']['local']['database']['username'],
        'PASSWORD': CFG['env']['local']['database']['password'],
        'HOST': CFG['env']['local']['database']['host'],
        'PORT': CFG['env']['local']['database']['port'],
    }
}

STATIC_ROOT = ''
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'formatters': {
        'standard': {
            'format':
"%(levelname)s [%(asctime)s] (%(name)s.%(funcName)s:%(lineno)s) %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_PATH, 'logs/django.log'),
            'maxBytes': 250000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'parse_errors': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_PATH, 'logs/parse_error.log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'api': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'parser': {
            'handlers': ['parse_errors'],
            'level': 'DEBUG',
        },
    }
}
