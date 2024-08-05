from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('users.urls')),
    path('inbox/', include('inbox.urls')),

]
# used to serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
