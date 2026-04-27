from celery import Celery
from src.mail import create_message,mail
from asgiref.sync import async_to_sync

c_app=Celery()

c_app.config_from_object('src.config')


@c_app.task
def send_mail(recipients:list[str],subject:str,body:str):
    message=create_message(recipients=recipients,subject=subject,body=body)

    # mail.send_message(message)

    async_to_sync(mail.send_message)(message)

    return "Mail sent Successfully"