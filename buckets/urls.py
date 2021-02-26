from django.urls import path

from .views import UserBucketsListView, BucketDetailView, BucketEditView, BucketFileDeleteView

app_name = 'buckets'

urlpatterns = [
    path('dashboard/', UserBucketsListView.as_view(), name='dashboard'),
    path('bucket/<str:pk>/', BucketDetailView.as_view(), name='bucket'),
    path('bucket/<str:pk>/edit/', BucketEditView.as_view(), name='bucket-edit'),

    path('bucket/file/<str:pk>/delete/', BucketFileDeleteView.as_view(), name='bucket-file-delete'),
]
