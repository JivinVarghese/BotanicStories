# botanic/urls.py
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
                  path('', views.home, name='home'),
                  path('create_post/', views.create_post, name='create_post'),
                  path('post/<int:post_id>/', views.view_post, name='view_post'),
                  path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
                  path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
                  path('comments/', views.comments, name='comments'),
                  path('post/<int:post_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
                  path('post/<int:post_id>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
                  path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
                  path('profile/<str:username>/', views.user_profile, name='user_profile'),
                  path('profile/<str:username>/about/', views.about_user, name='about_user'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
