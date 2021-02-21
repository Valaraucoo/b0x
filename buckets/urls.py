from django.urls import path

from .views import UserBucketsListView, BucketDetailView

app_name = 'buckets'

urlpatterns = [
    path('dashboard/', UserBucketsListView.as_view(), name='dashboard'),
    path('bucket/<str:pk>/', BucketDetailView.as_view(), name='bucket'),
]
