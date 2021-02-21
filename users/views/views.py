from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.views import generic

from users import forms
from users import models
from users.views import BaseAuthView

from users.emails.factory import AccountActivationEmailFactory

from utils.token import account_activation_token


class SignInView(BaseAuthView):
    template_name = "users/signin.html"
    form_class = forms.LoginForm

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        form = self.get_form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = None

            if email and password:
                user = authenticate(request, email=email, password=password)

            if user and user.is_active:
                login(request, user)
                if 'remember' in request.POST:
                    request.session['email'] = email
                    request.session['password'] = password
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)

                if request.user.is_authenticated:
                    messages.info(request, 'You are logged in!')
                    return redirect(settings.LOGIN_REDIRECT_URL)
            elif user and not user.is_avtive:
                messages.error('Activate you account.')
            else:
                messages.error(request, 'Try again')
        else:
            messages.error(request, 'Try again')

        context = self.get_context_data(*args, **kwargs)
        context['form'] = form
        context['errors'] = form.errors
        return render(request, self.template_name, context)


class RegistrationView(BaseAuthView):
    template_name = "users/register.html"
    form_class = forms.RegistrationForm

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

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
        else:
            messages.error(request, 'Try again')

        context = self.get_context_data(*args, **kwargs)
        context['form'] = form
        context['errors'] = form.errors
        return render(request, self.template_name, context)


class ActivateAccount(generic.View):
    template_name = 'users/activation_invalid.html'

    def get(self, request, uid, token, *args, **kwargs):
        uid_decoded = force_text(urlsafe_base64_decode(uid))
        user = models.User.objects.get(pk=uid_decoded)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.info(request, 'Your account has been activated!')
            return redirect('users:dashboard')
        return render(request, self.template_name)
