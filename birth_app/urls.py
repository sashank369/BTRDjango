from django.urls import path
from .views import create_birth, update_birth, search_birth

urlpatterns = [
    path('v1/registration/_create', create_birth),
    path('v1/registration/_update', update_birth),
    path('v1/registration/_search', search_birth),
]
