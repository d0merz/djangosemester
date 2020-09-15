import os
from celery import Celery
from celery.schedules import crontab
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusicProject.settings')

app = Celery('MusicProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_every_12_hour': {
        'task': 'account.tasks.send_spam',
        'schedule': crontab(hour='*/12', day_of_month='11-20'),
    }
}