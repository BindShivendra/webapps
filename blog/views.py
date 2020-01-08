from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from  django.utils import timezone

from .models import Post
from .forms import PostForm
from .utils import remove_image

class PostListView(ListView):
    model = Post
    template_name = 'list_view.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super(PostListView, self).get_queryset()
        for post in qs:
            post.body  = remove_image(post.body)
        return qs


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView ):
    model = Post
    # fields = ['title', 'body' ]
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    # fields = ['title', 'body' ]
    form_class = PostForm

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_view.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

def publish(request, slug):
    user = request.user
    post = Post.objects.get(slug=slug)
    if user.is_authenticated and post.user == user:
        post.publish_date = timezone.now()
        post.save()
    
    return redirect(reverse_lazy('blog:detail', args=[post.slug]))


list_view = PostListView.as_view()
detail_view = PostDetailView.as_view()
create_view = PostCreateView.as_view()
update_view = PostUpdateView.as_view()
delete_view = PostDeleteView.as_view()
user_posts = UserPostListView.as_view()