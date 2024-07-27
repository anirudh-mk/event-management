from django.dispatch import Signal
from django.dispatch import receiver
from django.core.mail import send_mail

from api.models import User
from decouple import config as decouple_config

# creat notification signal object
notification_signal = Signal()

# crate update notification signal object
update_notification_signal = Signal()


@receiver(notification_signal)
def send_event_notification(sender, instance, **kwargs):

    # access all users email as list
    users_emails = User.objects.all().values_list('email', flat=True)

    # send html message
    send_mail(
        subject=f'You are invited to {instance.title}',
        html_message=f'<h2>Invititon to {instance.title}</h2>'
                     f'<p>this is the invatation to {instance.title} on date {instance.date}</p>',
        message='',
        from_email=decouple_config('EMAIL_HOST_USER'),
        recipient_list=users_emails,
        fail_silently=False,
    )


@receiver(update_notification_signal)
def send_event_notification(sender, instance, **kwargs):
    # access all users email as list
    users_emails = User.objects.all().values_list('email', flat=True)

    # send html message
    send_mail(
        subject=f'Update on event {instance.title}',
        html_message=f'<h2>Update on event {instance.title}</h2>'
                     f'<p>There is an update on event {instance.title} on date {instance.date}</p>',
        message='',
        from_email=decouple_config('EMAIL_HOST_USER'),
        recipient_list=users_emails,
        fail_silently=False,
    )