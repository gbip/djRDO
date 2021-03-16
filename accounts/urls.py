from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# noinspection Pylint
app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/signin.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name="password_reset"),
    path('signup/', views.signup, name="signup")
]
