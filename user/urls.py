from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path(
        "get_user/<int:id>/", views.GetUpdateDeleteUserView.as_view(), name="get_user"
    ),
]
