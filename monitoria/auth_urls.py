from django.urls import include
from django.conf.urls import url
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    url(r'^', include('rest_auth.urls')),
    url(r'^rest_registration/', include('rest_auth.registration.urls')),
    url(r'^token_verify/', verify_jwt_token),
]