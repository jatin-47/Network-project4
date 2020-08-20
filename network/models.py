from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now=True)
    body = models.TextField(max_length=1000)
    likes = models.ManyToManyField(User , blank=True, related_name='liked')

class Follow(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.PositiveIntegerField(default=0)
    following = models.ManyToManyField(User , blank=True, related_name='followed')