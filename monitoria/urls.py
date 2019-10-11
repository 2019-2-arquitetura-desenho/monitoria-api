from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('monitoria.auth_urls')),
    url('^', include('django.contrib.auth.urls')),
]
