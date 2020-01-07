from django.contrib import admin

from .models import Post

# admin.site.register(Post)

from django_summernote.admin import SummernoteModelAdmin
# from .models import Post

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)

admin.site.register(Post, PostAdmin)
