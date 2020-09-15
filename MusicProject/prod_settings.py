
from .settings import DATABASES
import dj_database_url

ENVIRONMENT = 'production'
DEBUG = False
ALLOWED_HOSTS = ['django-sem-project.herokuapp.com', '127.0.0.1']

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
