from django.urls import path  # , include
from profiles import views

urlpatterns = [
    path('get_profile/', views.get_profile),
    path('set_profile/', views.set_profile),
    path('registration/', views.registration),
    path('get_professor/', views.get_professor),
    path('professor_classes/', views.professor_classes),
    path('get_student/', views.get_student),
    path('set_student/', views.set_student),
]
