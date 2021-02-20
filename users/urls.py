from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, TemplateView

from .forms import CustomPasswordResetForm, CustomPasswordResetConfirmForm
from .views import RegistrationView, ActivateAccount, SignInView

app_name = 'users'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('password-reset/', PasswordResetView.as_view(
        template_name="users/password-reset/form.html",
        success_url="/password-reset/send/",
        email_template_name="emails/users/password-reset/password_reset_email.html",
        form_class=CustomPasswordResetForm
    ), name='password-reset'),
    path('password-reset/confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(
        template_name="users/password-reset/confirm.html",
        success_url="/password-reset/complete/",
        form_class=CustomPasswordResetConfirmForm
    ), name='password_reset_confirm'),
    path('password-reset/send/', TemplateView.as_view(
        template_name="users/password-reset/send.html"
    ), name='password_reset_send'),
    path('password-reset/complete/', TemplateView.as_view(
        template_name="users/password-reset/complete.html"
    ), name='password_reset_complete'),
    path('activate/<slug:uid>/<slug:token>/', ActivateAccount.as_view(), name='activate'),
]
