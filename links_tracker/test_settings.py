import os
from pathlib import Path

INSTALLED_APPS = [
    'domains',
]
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'secret_key'
DEBUG = True
ROOT_URLCONF = 'links_tracker.urls'
REDIS_URL = os.environ.get("TEST_REDIS_URL", "redis://localhost:6379/1")
TEST_RUNNER = 'links_tracker.test_runner.NoDBTestRunner'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
