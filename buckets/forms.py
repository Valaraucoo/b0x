from django import forms

from buckets.models import Bucket
from users.forms import tailwind_form


class BucketForm(forms.ModelForm):
    class Meta:
        model = Bucket
        fields = ("name", "has_password", "password", "description")
        widgets = {
            "name": forms.TextInput(attrs={
                'class': tailwind_form,
                'placeholder': 'My bucket'
            }),
            "password": forms.PasswordInput(attrs={
                'class': tailwind_form,
                'placeholder': '**********'
            }),
            "description": forms.Textarea(attrs={
                'class': tailwind_form, 'cols': 30, 'rows': 5,
                'placeholder': 'Description'
            })
        }
