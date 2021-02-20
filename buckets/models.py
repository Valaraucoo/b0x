import os
import uuid

from django.db import models

from utils import get_file_path


class Bucket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', related_name='buckets', on_delete=models.CASCADE)
    password = models.CharField(max_length=50, null=True, blank=True)
    has_password = models.BooleanField(default=False)

    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-name', '-created_at',)

    def __str__(self):
        return f'Bucket: {self.name} / {self.user}'


class BucketFile(models.Model):
    filename = models.CharField(max_length=255, default='', blank=True)
    file = models.FileField(upload_to=get_file_path)
    bucket = models.ForeignKey('Bucket', related_name='files', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, **kwargs):
        if self.filename == '' or self.filename is None:
            self.filename = self.file.name.split('/')[-1]
        super().save(**kwargs)

    @property
    def size(self) -> int:
        return self.file.size

    @property
    def url(self) -> str:
        return self.file.url
    
    @property
    def extension(self):
        return os.path.splitext(self.file.name)[1]
