import os
from settings import *
from YamJam import yamjam

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

CFG = yamjam(os.path.join(PROJECT_PATH, 'etc/yamjam/config.yaml'))['litlong']

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = CFG['secret-key']

DATABASES = {
    'default': {
        'ENGINE': CFG['database']['engine'],
        'NAME': CFG['database']['name'],
        'USER': CFG['database']['username'],
        'PASSWORD': CFG['database']['password'],
        'HOST': CFG['database']['host'],
        'PORT': CFG['database']['port'],
    }
}

STATIC_ROOT = CFG['env']['production']['static-root']
STATIC_URL = '/static/'

GOOGLE_ANALYTICS_KEY = CFG['analytics-key']
