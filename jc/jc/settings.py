import os
from pathlib import Path
import dj_database_url


def _get_config(file_):
    import json, warnings
    try:
        with open(file_) as fd:
            return json.load(fd)
    except IOError as err:
        warnings.warn(err.args[1])
    except ValueError as err:
        warnings.warn(err)
    return {}


BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE =  os.environ.get('RAG_CONFIG', '/etc/jc.json')
CONFIG = {
    'DEFAULT_OLLAMA_MODEL': 'mistral',
    'DEFAULT_TEMPERATURE': .75,
    'DEFAULT_SQL_TEMPERATURE': .5,
    'DEFAULT_SUBQ_TEMPERATURE': .5,
    'DEFAULT_SIMILARITY_TOP_K': 2,
    'EMBED_DIM': 384,
    'OLLAMA_BASE_URL': 'http://localhost:11434',
}
CONFIG.update(_get_config(CONFIG_FILE))

SECRET_KEY = CONFIG.get('SECRET_KEY')
DEBUG = CONFIG.get('DEBUG')
ALLOWED_HOSTS = CONFIG.get('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'ui',
    'api',
    'django_tables2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jc.wsgi.application'

DATABASE_URL = CONFIG['DATABASE_URL']
DATABASES = {}
DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from django.utils.log import DEFAULT_LOGGING as LOGGING
LOGGING['loggers'].update({
    'httpcore': {
        'level': 'WARNING',
    },
    'httpx': {
        'level': 'WARNING',
    },
    'asyncio': {
        'level': 'WARNING',
    },
})

SOURCE_URL = CONFIG['SOURCE_URL']
SOURCE_TOKEN = CONFIG['SOURCE_TOKEN']
SOURCE_RETRY = {}
DATA_DIR = CONFIG['DATA_DIR']
SYSTEM_PROMPT = CONFIG['SYSTEM_PROMPT']
DEFAULT_OLLAMA_MODEL = CONFIG['DEFAULT_OLLAMA_MODEL']
DEFAULT_TEMPERATURE = CONFIG['DEFAULT_TEMPERATURE']
DEFAULT_SQL_TEMPERATURE = CONFIG['DEFAULT_SQL_TEMPERATURE']
DEFAULT_SUBQ_TEMPERATURE = CONFIG['DEFAULT_SUBQ_TEMPERATURE']
DEFAULT_SIMILARITY_TOP_K = CONFIG['DEFAULT_SIMILARITY_TOP_K']
DEFAULT_EMBED_DIM = CONFIG['EMBED_DIM']
OLLAMA_BASE_URL = CONFIG['OLLAMA_BASE_URL']
