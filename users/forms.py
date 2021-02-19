from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordResetForm, SetPasswordForm
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


tailwind_form = 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4' \
                ' leading-tight focus:outline-none focus:bg-white focus:border-gray-500'


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={
        'class': tailwind_form,
        'placeholder': 'Email address',
    }))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': tailwind_form,
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
                                     'class': tailwind_form, 'placeholder': 'John'
                                 }))
    last_name = forms.CharField(max_length=100,
                                min_length=2,
                                label='Enter first name',
                                widget=forms.TextInput(attrs={
                                    'class': tailwind_form, 'placeholder': 'Smith'
                                }))
    password = forms.CharField(max_length=100,
                               min_length=5,
                               required=True,
                               label='Password',
                               widget=forms.PasswordInput(attrs={
                                   'class': tailwind_form, 'placeholder': 'Password',
                               }))
    password2 = forms.CharField(max_length=100,
                                required=True,
                                min_length=5,
                                label='Confirm Password',
                                widget=forms.PasswordInput(attrs={
                                    'class': tailwind_form, 'placeholder': 'Confirm Password',
                                }))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            self.add_error('password2', 'Two password fields must match!')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        qs = User.objects.filter(email=email)
        if qs.count():
            raise forms.ValidationError('User with this email already exists!')
        return email


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=100,
                             required=True,
                             help_text='Required',
                             error_messages={'required': 'Sorry, you will need type an unique email address'},
                             widget=forms.EmailInput(attrs={
                                 'class': tailwind_form, 'placeholder': 'Email address'
                             }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if not user:
            raise forms.ValidationError('Unfortunately we can not find that email address')
        return email


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=100,
                                    min_length=5,
                                    required=True,
                                    label='Password',
                                    widget=forms.PasswordInput(attrs={
                                        'class': tailwind_form, 'placeholder': 'Password',
                                    }))
    new_password2 = forms.CharField(max_length=100,
                                    min_length=5,
                                    required=True,
                                    label='Password',
                                    widget=forms.PasswordInput(attrs={
                                        'class': tailwind_form, 'placeholder': 'Password',
                                    }))
