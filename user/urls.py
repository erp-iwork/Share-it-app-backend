from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("auth/signup/", views.SignupUserView.as_view(), name="signup"),
    path("auth/login/", views.LoginAPIView.as_view(), name="login"),
    path("auth_user/", views.AuthUserAPIView.as_view(), name="auth_user"),
    path("user/<int:id>/", views.UpdateDeleteUserView.as_view(), name="get_user"),
    path("user/follow/", views.FollowAPIView.as_view(), name="user_follow"),
    path(
        "user/unfollow/<int:following>",
        views.UnfollowAPIView.as_view(),
        name="user_unfollow",
    ),
]
