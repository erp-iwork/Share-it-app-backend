from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("auth/signup/", views.SignupUserView.as_view(), name="signup"),
    path("auth/login/", views.LoginAPIView.as_view(), name="login"),
    path("auth_user/", views.AuthUserAPIView.as_view(), name="auth_user"),
    path("user/<int:id>/", views.UpdateDeleteUserView.as_view(), name="get_user"),
    path("user/rating/", views.RagingAPIView.as_view(), name="user_rating"),
    path("user/profile/", views.PrifileAPIView.as_view(), name="user_Profile"),
    path(
        "user/add/profile/",
        views.AddProfileInfoAPIView.as_view(),
        name="add_Profile_info",
    ),
    path("user/follow/", views.FollowAPIView.as_view(), name="user_follow"),
    path(
        "user/unfollow/<int:following>",
        views.UnfollowAPIView.as_view(),
        name="user_unfollow",
    ),
]
