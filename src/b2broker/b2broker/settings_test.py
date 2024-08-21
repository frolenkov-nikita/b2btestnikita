from .settings import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["MYSQL_DATABASE"],
        "USER": os.environ["MYSQL_USER"],
        "PASSWORD": os.environ["MYSQL_PASSWORD"],
        "HOST": os.environ["MYSQL_HOST"],
        "PORT": os.environ["MYSQL_PORT"],
        "TEST": {
            # to make our life with mysql on compose simpler
            "NAME": os.environ["MYSQL_DATABASE"],
        },
    }
}
