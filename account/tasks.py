from __future__ import absolute_import, unicode_literals

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader

from MusicProject.celery import app
from MusicProject.settings import DEFAULT_FROM_EMAIL


@app.task
def send_mail_task(subject_template_name, email_template_name, context,
                   from_email, to_email, html_email_template_name):
    PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )


@app.task
def send_spam():
    for user in User.objects.filter(is_active=True):
        send_mail(
            'Рассылка',
            'Рассылка каждые 12 часов',
            DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
