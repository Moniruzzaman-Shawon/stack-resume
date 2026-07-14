import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "config.test_settings"
django.setup()
