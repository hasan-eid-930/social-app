from django.urls import include, path
from .views import *
urlpatterns = [
    path('', home,name='home'),
    path('post/create/', post_create,name='post-create'),
    path('post/delete/<pk>/', post_delete,name='post-delete'),
    path('post/edit/<pk>/', post_edit,name='post-edit'),
    path('post/<pk>/', post_page,name='post'),
]