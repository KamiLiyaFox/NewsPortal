from datetime import timedelta
from celery import shared_task
import time
from datetime import date, timedelta
import datetime
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime
from django.core.mail import EmailMultiAlternatives
from .signals import *
from .models import *
from django.utils.datetime_safe import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
import logging
from datetime import datetime


# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")
#
#
# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)

# @shared_task
# def my_task(news_id):
#     print('I am task and i am work')
@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def my_task():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = News.objects.filter(date_pub__gte=last_week)
    # print(f'{posts}')
    categories = set(posts.values_list('category__name', flat=True))
    print(f'{categories}')
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    print(f'{subscribers}')
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Публикации за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# @shared_task
# def complete_order(oid):
#     order = Order.objects.get(pk=oid)
#     order.complete = True
#     order.save()
#
# @shared_task
# def clear_old():
#     old_orders = Order.objects.all().exclude(time_in__gt =
#                         datetime.now() - timedelta(minutes = 5))
#     old_orders.delete()