from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.views import generic

from users import forms
from users import models
from users.views import BaseAuthenticationView

from users.emails.factory import AccountActivationEmailFactory

from utils.token import account_activation_token


class RegistrationView(BaseAuthenticationView):
    template_name = "users/register.html"
    form_class = forms.RegistrationForm

    def process_post_request(self, request, *args, **kwargs) -> None:
        form = self.get_form_class(request.POST)
        if form.is_valid():
            data = request.POST
            if data.get('agree') == 'on':
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.is_active = False
                user.save()

                AccountActivationEmailFactory(user, request, email_to=[user.email]).send()
                messages.info(request, 'Activate your account!')
                return redirect('/')


class ActivateAccount(generic.View):
    def get(self, request, uid, token, *args, **kwargs):
        uid_decoded = force_text(urlsafe_base64_decode(uid))
        user = models.User.objects.get(pk=uid_decoded)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('/dashboard/')
        return render(request, 'users/activation_invalid.html')



