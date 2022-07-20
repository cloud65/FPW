from datetime import datetime, timedelta
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from news.models import Post
from news_paper import settings


def get_url(post):
    domain = Site.objects.get_current().domain
    return f'http://{domain}/view/{post.pk}'


def send_new_categories(post_id):
    post = Post.objects.get(pk=post_id)
    categories = list(post.category.all())
    users = set()
    for cat in categories:
        users = users | set(list(cat.subscribers.all()))
    for user in list(users):
        html_content = render_to_string(
            'subscribes/new-post.html',
            {
                'username': user.username,
                'url': get_url(post),
                'post': post,
                'str_type': 'новость' if post.type_post == 1 else 'статья'
            }
        )
        msg = EmailMultiAlternatives(
            subject=post.title,
            body=html_content,  # это то же, что и message
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def send_new_week_categories():
    domain = Site.objects.get_current().domain
    title = 'Новые публикации за неделю'
    date_min = datetime.now(tz=timezone.utc) - timedelta(days=7)
    posts = Post.objects.filter(date_create__gte=date_min)
    # Выборку ниже я бы предпочел выбрать одним пакетом запросов, но незнаю как.
    # Поэтому разбиваю на for'ы
    categories = set()
    for post in posts:
        categories = categories | set(post.category.all())

    users = set()
    for cat in categories:
        users = users | set(list(cat.subscribers.all()))

    for user in users:
        user_posts = Post.objects.filter(category__in=user.subscribers.all(), id__in=posts.all()).distinct().all()
        html_content = render_to_string(
            'subscribes/week-new-post.html',
            {
                'username': user.username,
                'domain': domain,
                'posts': user_posts,
                'title': title
            }
        )
        msg = EmailMultiAlternatives(
            subject=title,
            body=html_content,  # это то же, что и message
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
