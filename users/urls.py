from django.urls import path
from .views import RegistrationView, ActivateAccount

app_name = 'users'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<slug:uid>/<slug:token>/', ActivateAccount.as_view(), name='activate')
]
