from django.shortcuts import render
from Email.email_config import *
from django.core.mail import EmailMultiAlternatives
from settings import EMAIL_HOST_USER

class ShootMail():
    def __init__(self, **kwargs):
	self.kwargs = kwargs

    def shoot_email(self):
        html_content = EMAIL['header'] + self.kwargs['body'] + EMAIL['footer']
        msg = EmailMultiAlternatives(self.kwargs['subject'], html_content, EMAIL_HOST_USER, [self.kwargs['email']])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


