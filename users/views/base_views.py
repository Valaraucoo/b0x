import abc
from typing import Optional

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import generic

from django import forms as django_forms

from core import settings


class BaseAuthenticationView(generic.View):
    template_name: str
    form_class = None

    def get_context_data(self, *args, **kwargs):
        return {
            'form': self.get_form_class(*args, **kwargs)
        }

    def get_form_class(self, *args, **kwargs):
        return self.form_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        context = self.get_context_data(*args, **kwargs)

        email = request.session.get('email')
        password = request.session.get('password')
        user = None

        if email and password:
            user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            if request.user.is_authenticated:
                messages.info(request, 'You are logged in!')
                return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        self.process_post_request(request, *args, **kwargs)

        context = self.get_context_data(*args, **kwargs)
        return render(request, self.template_name, context)

    @abc.abstractmethod
    def process_post_request(self, request, *args, **kwargs) -> None:
        pass
