from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import *
from .tasks import my_task, send_notifications


@receiver(post_save, sender=News)
def notify_about_new_post(sender, instance, created, **kwargs):
    print('Добавлена публикация', instance)
    if created==True:
        categories = instance.category
        subscribers: list[str] = []
        subscribers += categories.subscribers.all()

        subscribers = [s.email for s in subscribers]
        send_notifications.delay(instance.preview(), instance.pk, instance.title, subscribers)


# @receiver(post_save, sender=News)
# def news_created(instance, created, **kwargs):
#     print('Добавлена публикация', instance)
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscribers__category=instance.category
#     ).values_list('email', flat=True)
#
#     subject = f'Новая публикация в категории {instance.news}'
#
#     text_content = (
#         f'Заголовок: {instance.name}\n'
#         f'Содержание: {instance.preview}\n\n'
#         f'Ссылка на публикацию: http://127.0.0.1{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Заголовок: {instance.name}<br>'
#         f'Содержание: {instance.preview}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на публикацию</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
# @receiver(post_save, sender=News)
# def test_signal(sender, instance, **kwargs):
#     print(f'I am signal!!!')
