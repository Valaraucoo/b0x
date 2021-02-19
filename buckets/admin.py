from django.contrib import admin

from .models import Bucket, BucketFile


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    pass


@admin.register(BucketFile)
class BucketFileAdmin(admin.ModelAdmin):
    pass
