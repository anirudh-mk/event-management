from django.dispatch import Signal
from django.dispatch import receiver
from django.core.mail import send_mail

from api.models import User

notification_signal = Signal()


@receiver(notification_signal)
def send_event_notification(sender, instance, **kwargs):
    users = User.objects.all()
    email_list = [user.email for user in users]
    send_mail(
        subject=f'You are invited to {instance.title}',
        html_message=f'<h2>Invititon to {instance.title}</h2>'
                     f'<p>this is the invatation to {instance.title} on date {instance.date}</p>',
        message='',
        from_email='anirudhmk123@gmail.com',
        recipient_list=email_list,
        fail_silently=False,
    )