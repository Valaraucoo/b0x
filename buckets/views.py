from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import reverse

from buckets import models


class BucketDetailView(DetailView):
    template_name = "buckets/bucket.html"
    model = models.Bucket
    context_object_name = "bucket"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        files = self.get_object().files.all()
        params = self.request.GET

        updated_at = params.get('updated_at')
        if updated_at:
            value = int(updated_at)
            if value > 0:
                files = files.order_by('updated_at')
            else:
                files = files.order_by('-updated_at')

        filename = params.get('filename')
        if filename:
            value = int(filename)
            if value > 0:
                files = files.order_by('filename')
            else:
                files = files.order_by('-filename')

        size = params.get('size')
        if size:
            value = int(size)
            if value > 0:
                files = sorted(files, key=lambda file: file.size)
            else:
                files = sorted(files, key=lambda file: -file.size)

        filetype = params.get('type')
        if filetype:
            value = int(filetype)
            if value > 0:
                files = sorted(files, key=lambda file: file.extension[1:])
            else:
                files = sorted(files, key=lambda file: file.extension[1:], reverse=True)

        context.update({
            'files': files
        })
        return context

    def get(self, request, pk, *args, **kwargs):
        bucket = self.get_object()
        response = super().get(request, pk, *args, **kwargs)
        if request.user == bucket.user:
            return response

        if not bucket.has_password:
            return response

        password = request.COOKIES.get(f'bucket-password-{bucket.id}')
        if password == bucket.password:
            return response

        url = reverse('password-bucket-check', args=(bucket.id,))
        bucket_url = reverse('buckets:bucket', args=(bucket.id,))

        return HttpResponseRedirect(url + f"?next={bucket_url}")

    def post(self, request, pk, *args, **kwargs):
        response = self.get(request, pk, *args, **kwargs)

        verbose_filename = request.POST.get('filename')
        file = request.FILES.get('uploadFile')

        if verbose_filename and file:
            bucket = self.get_object()
            bucket_file = models.BucketFile.objects.create(
                verbose_filename=verbose_filename,
                file=file,
                bucket=bucket
            )
            bucket_file.save()
            messages.info(request, 'Success')
        else:
            messages.error(request, 'Something went wrong!')

        return response


class UserBucketsListView(LoginRequiredMixin, ListView):
    template_name = "buckets/dashboard.html"
    model = models.Bucket
    context_object_name = "buckets"

    def get_queryset(self):
        return models.Bucket.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'user': self.request.user,
        })
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        if 'name' in data:
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            has_password = request.POST.get('has_password', False)
            password = ''
            if has_password:
                password = request.POST.get('password')
            try:
                instance = self.model.objects.create(
                    name=name,
                    description=description,
                    has_password=bool(has_password),
                    password=password,
                    user=request.user
                )
                instance.save()
                messages.info(request, "A new bucket has been created successfully")
            except:
                messages.error(request, "Error occured. Try again!")
        else:
            messages.error(request, "A bucket name is required")

        return super().get(request, *args, **kwargs)
