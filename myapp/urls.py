# botanic/urls.py
from django.urls import path
from .views import base, register, custom_login, custom_logout

urlpatterns = [
    path('', base, name='home'),
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout')
]
