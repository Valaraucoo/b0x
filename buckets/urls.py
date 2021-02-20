from django.urls import path

from .views import UserBucketsListView

app_name = 'buckets'

urlpatterns = [
    path('dashboard/', UserBucketsListView.as_view(), name='dashboard'),
]
