from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField

from .utils import slug_generator

USER = get_user_model()

class PostManager(models.Manager):

    def published(self):
        return self.get_queryset().filter(publish_date__isnull=False)

class Post(models.Model): 
    user    = models.ForeignKey(USER, on_delete=models.CASCADE)
    title  = models.CharField(max_length=120)
    slug   = models.SlugField(unique=True, null=True, blank=True) 
    body  = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    objects = PostManager()

    class Meta:
        ordering = ['-publish_date', '-updated', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('blog:detail', kwargs={'slug': self.slug})


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)

pre_save.connect(pre_save_receiver, sender=Post)