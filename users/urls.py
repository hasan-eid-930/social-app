from django.urls import include, path
from .views import *

urlpatterns = [
    path('', profile,name='profile'),
    path('edit/', profile_edit,name='profile-edit'),
    path('onboarding/', profile_edit,name='profile-onboarding'),
    path('delete/', profile_delete,name='profile-delete'),
    path('<username>/', profile,name='user-profile'),
    
]