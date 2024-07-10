# botanic/urls.py
from django.urls import path
from .views import base

urlpatterns = [
    path('', base, name='base'),
]
