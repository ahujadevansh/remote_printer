from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as users_views

app_name = 'users'

urlpatterns = [
    path('register/', users_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),


    path('profile/', users_views.ProfileView.as_view(), name='profile'),
]
