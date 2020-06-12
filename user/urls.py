from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("signup/", views.SignupUserView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("auth_user/", views.AuthUserAPIView.as_view(), name="auth_user"),
    path("get_user/<int:id>/", views.UpdateDeleteUserView.as_view(), name="get_user"),
]
