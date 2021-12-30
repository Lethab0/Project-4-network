# Generated by Django 4.0 on 2021-12-22 11:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_liked_delete_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liked',
            name='who_liked',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]