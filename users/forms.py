from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'password',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


tailwind_form = 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 ' \
                'placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:shadow-outline-blue ' \
                'focus:border-blue-300 focus:z-10 sm:text-sm sm:leading-5'

tailwind_form2 = 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 ' \
                 'placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 ' \
                 'focus:border-indigo-500 focus:z-10 sm:text-sm'


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={
        'class': tailwind_form,
        'placeholder': 'Email address',
    }))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': tailwind_form2,
        'placeholder': 'Password',
    }))


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=100,
                             required=True,
                             help_text='Required',
                             error_messages={'required': 'Sorry, you will need type an unique email address'},
                             widget=forms.EmailInput(attrs={
                                 'class': tailwind_form, 'placeholder': 'Email address'
                             }))
    first_name = forms.CharField(max_length=100,
                                 min_length=2,
                                 label='Enter first name',
                                 widget=forms.TextInput(attrs={
                                     'class': tailwind_form, 'placeholder': 'First name'
                                 }))
    last_name = forms.CharField(max_length=100,
                                min_length=2,
                                label='Enter first name',
                                widget=forms.TextInput(attrs={
                                    'class': tailwind_form, 'placeholder': 'First name'
                                }))
    password = forms.CharField(max_length=100,
                               required=True,
                               label='Password',
                               widget=forms.PasswordInput(attrs={
                                   'class': tailwind_form2, 'placeholder': 'Password',
                               }))
    password2 = forms.CharField(max_length=100,
                                required=True,
                                label='Confirm Password',
                                widget=forms.PasswordInput(attrs={
                                    'class': tailwind_form2, 'placeholder': 'Confirm Password',
                                }))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')
