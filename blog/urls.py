from django.urls import path

from .views import list_view, detail_view, create_view
from .views import update_view, delete_view

app_name = 'blog'

urlpatterns = [
    path('all', list_view, name='list'),
    path('new', create_view , name='create'),
    path('<str:slug>/edit', update_view , name='update'),
    path('<str:slug>/delete', delete_view , name='delete'),
    path('<str:slug>', detail_view , name='detail'),
    path('', list_view, name='list'),
]