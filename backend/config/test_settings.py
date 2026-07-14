import os
from config.settings import *  # noqa: F401, F403

os.environ.setdefault("DJANGO_SECRET_KEY", "test-secret-key-not-for-production")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "test-secret-key-not-for-production")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {},
}
