# Generated by Django 3.1.6 on 2021-02-20 11:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0002_auto_20210220_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='password',
            field=models.CharField(default='11111', max_length=50, validators=[django.core.validators.MinLengthValidator(5)]),
            preserve_default=False,
        ),
    ]