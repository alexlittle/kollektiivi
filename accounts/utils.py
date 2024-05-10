import datetime

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings


def send_invoice_email(to_email, subject, body, attachment):

    body = body + "\n\nKatso liitteenä... "
    kwargs = dict(
        to=[to_email],
        bcc=[settings.DEFAULT_FROM_EMAIL],
        from_email=settings.DEFAULT_FROM_EMAIL,
        subject=subject,
        body=body,
    )
    message = EmailMultiAlternatives(**kwargs)
    message.attach_file(attachment)
    message.send()
