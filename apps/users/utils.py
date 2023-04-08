from django.conf import settings
from django.core.mail import send_mail


def send_sms_by_email(email, code):
    subject = f'Autorization by email verification code'
    message = f'\n\nYour verification code : {code}\n\n'
    print(message)
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    print(mail_sent, 'send_sms_by_email')
    return mail_sent
