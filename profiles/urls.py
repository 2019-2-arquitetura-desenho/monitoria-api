from django.urls import include, path
from profiles import views

urlpatterns = [
    path('set_profile/', views.set_profile),
]