from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields =['title', 'body' ]
        widgets = {
            'body': SummernoteWidget(),
            # 'title': SummernoteInplaceWidget(),
        }