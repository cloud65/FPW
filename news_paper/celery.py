import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_paper.settings')

app = Celery('news_paper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Рассылка еженедельной сводки новостей
app.conf.beat_schedule = {
    'send_new_week_categories_every_monday_8am': {
        'task': 'news.tasks.send_new_week_categories',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}