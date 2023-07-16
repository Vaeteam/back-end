from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from datetime import datetime, timedelta
from rest_framework import exceptions
from .models import CustomUser
import jwt


# TODO FOR EMAIL ACCOUNT CONFIRMATION

def gen_email_confirmation_token(user, user_email):
    token = jwt.encode({'id': user.id, 'type': 'email_confirm_signup', 'username': user.first_name, 'email': user_email,
                        'exp': datetime.utcnow() + timedelta(hours=1)}, settings.SECRET_KEY, algorithm='HS256')
    return token

def send_email_account_confirm(user, user_email):
    try:
        current_site = settings.FRONTEND_AUTH_URL
        mail_subject = 'Kích hoạt tài khoản Weteach'
        email_recepient = user_email
        msg_html = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': gen_email_confirmation_token(user, user_email),
        })
        email = EmailMessage(mail_subject, msg_html, to=[email_recepient])
        email.content_subtype = 'html'  # this is required because there is no plain text email message
        email.send(fail_silently=True)
    except Exception as e:
        print("Error send_email_account_confirm " , e)
        raise exceptions.AuthenticationFailed({'error': 'send message is not working'})

def check_email_account_confirmation_token(uidb64, token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user_id_token = str(payload['id'])
        email = payload.get("email")
        if payload['type'] != 'email_confirm_signup':
            raise exceptions.AuthenticationFailed({'error': 'token is not valid'})
    except:
        raise exceptions.AuthenticationFailed({'error': 'token is expire, login again'})
    try:
        user_id_uidb64 = force_str(urlsafe_base64_decode(uidb64))
    except:
        raise exceptions.AuthenticationFailed({'error': 'uidb64 is not valid'})

    if user_id_uidb64 != user_id_token:
        raise exceptions.AuthenticationFailed({'error': 'user id is not the same'})

    try:
        user = CustomUser.objects.get(id=user_id_token)
    except:
        raise exceptions.AuthenticationFailed({'error': 'user is not exist'})

    user.is_active = True
    user.auth_google = True
    user.email = email
    user.save()

    return user


# TODO FOR RESET PASSWOR
def gen_password_reset_token(user):
    token = jwt.encode({'id': user.id, 'type': 'email_password_reset', 'username': user.first_name, 'email': user.email,
                        'exp': datetime.utcnow() + timedelta(minutes=15)}, settings.SECRET_KEY, algorithm='HS256')
    return token

def send_email_password_reset(user):
    try:
        current_site = settings.FRONTEND_AUTH_URL
        mail_subject = 'Reset your Weteach password.'
        email_recepient = user.email
        msg_html = render_to_string('acc_password_reset.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': gen_password_reset_token(user),
        })
        email = EmailMessage(mail_subject, msg_html, to=[email_recepient])
        email.content_subtype = "html"
        email.send(fail_silently=True)
    except:
        raise exceptions.AuthenticationFailed({'error': 'send message is not working'})


def check_email_reset_password_token(uidb64, token, password):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user_id_token = str(payload['id'])
        if payload['type'] != 'email_password_reset':
            raise exceptions.AuthenticationFailed({'error': 'token is not valid'})
    except:
        raise exceptions.AuthenticationFailed({'error': 'token is expire, login again'})
    try:
        user_id_uidb64 = force_str(urlsafe_base64_decode(uidb64))
    except:
        raise exceptions.AuthenticationFailed({'error': 'uidb64 is not valid'})

    if user_id_uidb64 != user_id_token:
        raise exceptions.AuthenticationFailed({'error': 'user id is not the same'})

    try:
        user = CustomUser.objects.get(id=user_id_token)
    except:
        raise exceptions.AuthenticationFailed({'error': 'user is not exist'})

    user.set_password(password)
    if not user.is_active:
        user.is_active = True
        user.auth_google = True
    user.save()

    return user

