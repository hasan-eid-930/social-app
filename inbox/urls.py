from django.urls import include, path
from .views import *







urlpatterns = [
    path('', inbox,name='inbox'),
    path('c/<conversation_id>/', inbox,name='conversation'),
    path('search_user/', search_user,name='search-user'),
    path('new-message/<recipient_name>/', new_message,name='new-message'),
    path('send-reply/<conversation_id>/', send_reply,name='send-reply'),
    path('notify/<conversation_id>/', check_notification,name='check-notification'),
    path('inbox_notify/', inbox_notify,name='inbox-notify'),
]