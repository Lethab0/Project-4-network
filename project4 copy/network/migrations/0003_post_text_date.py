# Generated by Django 3.2 on 2021-06-28 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
