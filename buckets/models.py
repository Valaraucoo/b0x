import hashlib
import os
import uuid
from functools import reduce
from typing import Optional
from PIL import Image

from django.db import models
from django.utils.functional import cached_property

from utils import get_protected_file_path


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

    @property
    def short_description(self):
        if len(self.description) > 20:
            return self.description[:-18] + '...'
        return self.description

    @cached_property
    def password_hash(self) -> str:
        return hashlib.md5(self.password.encode()).hexdigest()

    @cached_property
    def size(self) -> int:
        try:
            return reduce(lambda a, b: a+b, [file.size for file in self.files.all()])
        except TypeError:
            return 0


class BucketFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    verbose_filename = models.CharField(max_length=255, default='', blank=True)

    filename = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=get_protected_file_path)
    bucket = models.ForeignKey('Bucket', related_name='files', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, **kwargs):
        self.filename = self.file.url.split('/')[-1]
        super().save(**kwargs)

    @property
    def public_filename(self) -> str:
        if self.verbose_filename != '':
            return self.verbose_filename
        return self.filename

    @property
    def is_protected(self) -> bool:
        return self.bucket.has_password

    @property
    def size(self) -> int:
        return round(self.file.size / 10e5, 2)

    @property
    def url(self) -> str:
        return self.file.url
    
    @property
    def extension(self) -> str:
        return os.path.splitext(self.file.name)[1]

    @property
    def is_image(self) -> bool:
        return self.extension in ['.jpg', '.png']

    @property
    def width(self) -> Optional[int]:
        if self.is_image:
            image = Image.open(self.file.file)
            return image.size[0]
        return None

    @property
    def height(self) -> Optional[int]:
        if self.is_image:
            image = Image.open(self.file.file)
            return image.size[1]
        return None
