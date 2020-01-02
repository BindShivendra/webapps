from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'list_view.html'
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'body' ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'body' ]

    

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:list')

list_view = PostListView.as_view()
detail_view = PostDetailView.as_view()
create_view = PostCreateView.as_view()
update_view = PostUpdateView.as_view()
delete_view = PostDeleteView.as_view()