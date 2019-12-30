from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'list_view.html'


class PostDetailView(DetailView):
    model = Post


list_view = PostListView.as_view()
detail_view = PostDetailView.as_view()