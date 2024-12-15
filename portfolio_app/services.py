from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from django.conf import settings

def send_email(html_template, subject, email, context=None):
    if context is None:
        context = {}
    html_message = render_to_string(html_template, context)

    email = EmailMultiAlternatives(
        subject = subject,
        body = html_message,
        from_email = settings.EMAIL_HOST_USER,
        to = [email],
    )
    email.attach_alternative(html_message, "text/html")

    email.send()