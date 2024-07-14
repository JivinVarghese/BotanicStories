# botanic/urls.py
from django.urls import path, include

from . import views
from .views import base

urlpatterns = [
    path('', base, name='base'),
    path('comments/', views.comments, name='comments'),
]
