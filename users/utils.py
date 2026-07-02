from django.core.mail import send_mail
from django.conf import settings
import datetime
# login user
def logMail(fullname,email):
    subject = "Login Confirmation"
    message = f'''
                Hi {fullname},
                We observe that a device login to this account on {(datetime.date.today())}.
                
                '''
    
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)
# onboarding
def sendMail(fullname,email):
    subject = "Welcome to Elixir Application, please click link to complete registration"
    message = f'''
                Hi {fullname},
                Thank you for registering with us.
                
                '''
    
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)