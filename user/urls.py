from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("auth/signup/", views.SignupUserView.as_view(), name="signup"),
    path("users/<str:id>", views.UserCRUD.as_view()),
    path("auth/login/", views.LoginAPIView.as_view(), name="login"),
    path(
        "user_profile/", views.AuthUserAPIView.as_view(), name="profile"
    ),  # gives all user info data
    path(
        "user/<uuid:id>/", views.UpdateDeleteUserView.as_view(), name="get_user"
    ),  # Send user uuid along with url user/uuid/
    path("user/rating/", views.RatingAPIView.as_view(), name="user_rating"),
    path(
        "user/rating/<int:ratingId>/", views.RatingAPIView.as_view(), name="user_rating"
    ),
    path(
        "user/profile/<str:user>/", views.ProfileAPIView.as_view(), name="user_profile"
    ),  # Send user uuid alliong url user/profile/uuid/
    path("user/follow/", views.FollowAPIView.as_view(), name="user_follow"),
    path("user/unfollow/", views.UnfollowAPIView.as_view(), name="user_unfollow",),
]
