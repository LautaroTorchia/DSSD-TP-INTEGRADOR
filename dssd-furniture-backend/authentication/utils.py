from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()

    @staticmethod
    def replace_html(keywords, text, values):
        keys_list = keywords.split('-')
        if len(keys_list) != len(values):
            raise ValueError("List of values ​​should contain {} elements!".format(len(keys_list)))
        l = ['{{#}}'.replace('#', n) for n in keys_list]
        for i in range(len(l)):
            text = text.replace(l[i], values[i])
        return text

class StandardSend:
    @staticmethod
    def send_email(subject, html_content, from_email, to):
        email = EmailMultiAlternatives(subject, 'text_content', from_email, [to])
        email.attach_alternative(html_content, "text/html")
        EmailThread(email).start()