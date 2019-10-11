from django.urls import include, path
from profiles import views

urlpatterns = [
    path('get_profile/', views.get_profile),
    path('set_profile/', views.set_profile),
    path('registration/', views.registration),
]