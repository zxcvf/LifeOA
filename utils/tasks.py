from __future__ import absolute_import, unicode_literals
from celery import shared_task
from utils.email_util import EmailHelper


@shared_task(ignore_result=True)
def send_email(content, to_address, subject, attachment=None):
    email = EmailHelper()
    email.set_content(
        content,
        to_address,
        subject,
        attachment
    )
    email.send()