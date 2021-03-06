# Generated by Django 4.0 on 2021-12-16 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_rename_follow_user_following_user_followers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='liked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0)),
                ('liked_post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='network.post')),
                ('who_liked', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Following',
        ),
    ]
