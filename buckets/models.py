import uuid

from django.db import models

from utils import get_file_path


class Bucket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', related_name='buckets', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-name', '-created_at',)

    def __str__(self):
        return f'Bucket: {self.name} / {self.user}'


class BucketFile(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_file_path)
    bucket = models.ForeignKey('Bucket', related_name='files', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
