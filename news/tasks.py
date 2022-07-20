from celery import shared_task

import news.subscribers as subscribers

@shared_task
def send_new_categories(post_id):
    subscribers.send_new_categories(post_id)


@shared_task
def send_new_week_categories():
    subscribers.send_new_week_categories()