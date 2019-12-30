from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()

class PostManager(models.Manager):

    def published(self):
        return self.get_queryset().published()

class Post(models.Model): 
    user    = models.ForeignKey(USER, on_delete=models.CASCADE)
    title  = models.CharField(max_length=120)
    slug   = models.SlugField(unique=True) 
    body  = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    objects = PostManager()

    class Meta:
        ordering = ['-publish_date', '-updated', '-created_at']

    def __str__(self):
        return self.title