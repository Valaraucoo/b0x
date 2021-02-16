import abc
from typing import List, Dict, Any

from django.conf import settings
from django.core import mail
from django.template import loader


class EmailFactoryInterface(abc.ABC):
    subject: str
    email_template_name: str

    def __init__(self, email_to: List[str] = None, email_from: str = settings.SENDER_EMAIL,
                 cc: List[str] = None, bcc: List[str] = None, reply_to: List[str] = None):
        self.email_to: List[str] = email_to or []
        self.email_from: str = email_from
        self.cc: List[str] = cc
        self.bcc: List[str] = bcc
        self.reply_to: List[str] = reply_to

    @abc.abstractmethod
    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        pass

    def create_email(self) -> mail.EmailMessage:
        context = self.get_context_data()
        body = loader.render_to_string(self.email_template_name, context)
        email_from = self.email_from or settings.SENDER_EMAIL
        message = mail.EmailMessage(self.subject, body, email_from, self.email_to,
                                    cc=self.cc, bcc=self.bcc, reply_to=self.reply_to)
        message.content_subtype = 'html'
        return message

    def send(self) -> None:
        self.create_email().send()
