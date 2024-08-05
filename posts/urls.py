from django.urls import include, path
from .views import *
urlpatterns = [
    path('', home,name='home'),
    path('category/<tag>/', home,name='category'),
    path('post/create/', post_create,name='post-create'),
    path('post/delete/<pk>/', post_delete,name='post-delete'),
    path('post/edit/<pk>/', post_edit,name='post-edit'),
    path('post/like/<pk>/', post_like,name='post-like'),
    path('post/<pk>/', post_page,name='post'),
    path('comment/create/<post_pk>/', comment_create,name='comment-create'),
    path('comment/delete/<pk>/', comment_delete,name='comment-delete'),
    path('comment/like/<pk>/', comment_like,name='comment-like'),
    path('reply/create/<post_pk>/<comment_pk>/', comment_create,name='reply-create'),
]