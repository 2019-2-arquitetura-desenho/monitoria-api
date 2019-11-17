from django.urls import include, path
from rest_framework import routers
from disciplines import views

router = routers.DefaultRouter()
router.register(r'class', views.ClassViewSet)
router.register(r'disciplines', views.DisciplineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get_discipline/', views.get_discipline),
    path('add_professor/', views.add_professor),
    path('remove_professor/', views.remove_professor),
    path('create_period/', views.create_period),
    path('register_discipline/', views.register_discipline),
    path('get_class_ranking/', views.get_class_ranking),
    path('get_student_rankings/', views.get_student_rankings),
    path('calculate_winners/', views.calculate_winners),
]
