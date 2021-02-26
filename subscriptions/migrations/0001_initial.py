# Generated by Django 3.1.6 on 2021-02-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=255)),
                ('subscription_id', models.CharField(blank=True, max_length=255, null=True)),
                ('subscribed_until', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
