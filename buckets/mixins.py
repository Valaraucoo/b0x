from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView

from buckets import models


class BucketOwnerPermissionMixin(DetailView):
    model = models.Bucket

    def dispatch(self, request, *args, **kwargs):
        bucket = self.get_object()
        response = super().dispatch(request, *args, **kwargs)
        if request.user == bucket.user:
            return response
        raise PermissionDenied('You do not have permission to edit the bucket.')
