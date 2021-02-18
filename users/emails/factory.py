from typing import Any, Dict
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from utils.emails import EmailFactoryInterface
from utils.token import account_activation_token


class AccountActivationEmailFactory(EmailFactoryInterface):
    subject = "Activate your Account"
    email_template_name = "emails/users/activate.html"

    def  __init__(self, user, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.request = request

    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        current_site = get_current_site(self.request)
        return {
            'domain': current_site.domain,
            'user': self.user,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': account_activation_token.make_token(self.user)
        }
