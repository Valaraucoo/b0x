from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from buckets import models


class UserBucketsListView(LoginRequiredMixin, ListView):
    template_name = "buckets/dashboard.html"
    model = models.Bucket

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
