from django.core.mail import send_mail

from django_snippets.settings import EMAIL_HOST_USER as sender
from celery import shared_task

@shared_task
def sendEmailInSnippetCreation(snippet_name, snippet_description, user_mail):
    if user_mail:
        subject = 'Snippet "' + snippet_name + '" created successfully'
        body = f'The snippet "{snippet_name}" was created with the following description: \n{snippet_description}'
        send_mail(subject, body, sender, [user_mail])