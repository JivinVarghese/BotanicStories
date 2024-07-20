# botanic/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import base, register, custom_login, custom_logout, user_analytics

urlpatterns = [
    path('', base, name='home'),
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('analytics/',user_analytics, name='analytics'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name="password_change.html"),
         name='password_change'),
    path('password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"),
         name='password_change_done'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name='reset_password'),
    path('reset_password_done/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name='password_reset_complete'),

]
