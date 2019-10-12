from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.sites.models import Site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('monitoria.auth_urls')),
    path('', include('profiles.urls')),
    url('^', include('django.contrib.auth.urls')),
]

site = Site.objects.get(id=1)
site.name = 'localhost:8000'
site.domain = 'localhost:8000'
site.save()
current_domain = 'localhost:8000'
