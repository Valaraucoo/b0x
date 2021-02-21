from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import TemplateView

from .storages import serve_protected_media_file, password_check_view, password_check_bucket_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="page/landing-page.html"), name='landing-page'),
    path('', include('users.urls', 'users')),
    path('', include('buckets.urls', 'buckets')),
    path('media/uploads/protected/<str:filename>/', serve_protected_media_file, name='protected-media'),
    path('password/media/<str:filename>/', password_check_view, name='password-check'),
    path('password/bucket/<str:pk>/', password_check_bucket_view, name='password-bucket-check'),
]


if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
