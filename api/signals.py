from django.dispatch import Signal
from django.dispatch import receiver
from django.core.mail import send_mail

from api.models import User
from decouple import config as decouple_config

notification_signal = Signal()
update_notification_signal = Signal()


@receiver(notification_signal)
def send_event_notification(sender, instance, **kwargs):
    users = User.objects.all()
    email_list = [user.email for user in users]
    send_mail(
        subject=f'You are invited to {instance.title}',
        html_message=f'<h2>Invititon to {instance.title}</h2>'
                     f'<p>this is the invatation to {instance.title} on date {instance.date}</p>',
        message='',
        from_email=decouple_config('EMAIL_HOST_USER'),
        recipient_list=email_list,
        fail_silently=False,
    )


@receiver(update_notification_signal)
def send_event_notification(sender, instance, **kwargs):
    users = User.objects.all()
    email_list = [user.email for user in users]
    send_mail(
        subject=f'Update on event {instance.title}',
        html_message=f'<h2>Update on event {instance.title}</h2>'
                     f'<p>There is an update on event {instance.title} on date {instance.date}</p>',
        message='',
        from_email=decouple_config('EMAIL_HOST_USER'),
        recipient_list=email_list,
        fail_silently=False,
    )