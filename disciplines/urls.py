from django.urls import include, path
from rest_framework import routers
from disciplines import views

router = routers.DefaultRouter()
router.register(r'class', views.ClassViewSet)
router.register(r'discipline', views.DisciplineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get_discipline/', views.get_discipline),
    path('add_professor/', views.add_professor),
    path('get_professor/', views.get_professor),
    path('remove_professor/', views.remove_professor),
]
