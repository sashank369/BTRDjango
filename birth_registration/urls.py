# birth_service/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('birth_app.urls')),
]
