from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Follow_database(models.Model):
    Person = models.OneToOneField(User, on_delete=models.CASCADE)
    Following = models.ManyToManyField('User', blank=True , related_name='Following')
    Followers = models.ManyToManyField('User', blank=True, related_name='Followers')
    
class Post(models.Model):
    Texter = models.ForeignKey(User, on_delete= models.CASCADE)
    text = models.CharField(null=False , max_length=30)
    text_date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    class meta:
        ordering = ('text_date',)
     
class liked(models.Model):
    liked_post = models.OneToOneField(Post , on_delete=models.CASCADE)
    who_liked = models.ManyToManyField(User, blank=True)
    likes = models.IntegerField(default=0)
