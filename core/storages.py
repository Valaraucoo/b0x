from django.http import FileResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, reverse

from django.contrib import messages

from buckets.models import BucketFile, Bucket
from utils import set_cookie


def serve_protected_media_file(request, filename):
    file = get_object_or_404(BucketFile, filename=filename)
    bucket = file.bucket

    response = FileResponse(file.file, )
    response["Content-Disposition"] = "filename=" + filename

    if request.user == bucket.user or not bucket.has_password:
        return response

    password = request.COOKIES.get(f'bucket-password-{bucket.id}')
    if password == bucket.password:
        return response

    url = reverse('password-check', args=(filename,))
    file_url = reverse('protected-media', args=(filename,))

    return HttpResponseRedirect(url + f"?next={file_url}")


def password_check_view(request, filename):
    file = get_object_or_404(BucketFile, filename=filename)
    bucket = file.bucket

    if request.user == bucket.user or not bucket.has_password:
        return redirect('protected-media')

    response = render(request, 'buckets/media-password.html', context={'bucket': bucket})
    response = check_password(request, response, bucket)
    return response


def password_check_bucket_view(request, pk):
    bucket = get_object_or_404(Bucket, pk=pk)

    if request.user == bucket.user or not bucket.has_password:
        return redirect('buckets:bucket', bucket.id)

    response = render(request, 'buckets/media-password.html', context={'bucket': bucket})
    response = check_password(request, response, bucket)
    return response


def check_password(request, response, bucket):
    password = request.COOKIES.get(f'bucket-password-{bucket.id}')
    if password == bucket.password:
        response = redirect('buckets:bucket', bucket.id)
        if request.GET.get('next'):
            response = redirect(request.GET.get('next'))
        response = set_cookie(response, f'bucket-password-{bucket.id}', bucket.password, days_expire=3)
        return response

    if request.method == 'POST':
        password = request.POST.get('password')
        if password and bucket.password == password:
            response = redirect('buckets:bucket', bucket.id)
            if request.GET.get('next'):
                response = redirect(request.GET.get('next'))
            response = set_cookie(response, f'bucket-password-{bucket.id}', bucket.password, days_expire=3)
            return response
        else:
            messages.error(request, 'Incorrect password')
    return response
