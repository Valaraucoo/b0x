from django.contrib import messages
from django.shortcuts import redirect

from core import settings

from users import forms
from users.views import BaseAuthenticationView

from users.emails.factory import AccountActivationEmailFactory


class RegistrationView(BaseAuthenticationView):
    template_name = "users/register.html"
    form_class = forms.RegistrationForm

    def process_post_request(self, request, *args, **kwargs) -> None:
        form = self.get_form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            AccountActivationEmailFactory(user, request, email_to=[user.email]).send()
            messages.info(request, 'Activate your account!')
            return redirect(settings.LOGIN_URL)
        else:
            messages.error(request, 'Something went wrong')
