# botanic/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.landing_page, name='landing_page'),
                  path('register/', views.register, name='register'),
                  path('login/', views.custom_login, name='login'),
                  path('logout/', views.custom_logout, name='logout'),
                  path('analytics/', views.user_analytics, name='analytics'),
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
                  path('home/', views.home, name='home'),
                  path('create_post/', views.create_post, name='create_post'),
                  path('post/<int:post_id>/', views.view_post, name='view_post'),
                  path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
                  path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
                  # path('comments/', views.comments, name='comments'),
                  path('post/<int:post_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
                  path('post/<int:post_id>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
                  path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
                  path('profile/<str:username>/', views.user_profile, name='user_profile'),
                  path('profile/<str:username>/about/', views.about_user, name='about_user'),
                  path('search/', views.search_posts, name='search_posts'),
                  path('bookmark/', views.bookmark_view, name='bookmark'),
                  path('like/', views.like_view, name='like_view'),
                  path('about/', views.about, name='about'),
                  path('contact/', views.contact_view, name='contact'),
                  path('library/', views.library, name='library')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

