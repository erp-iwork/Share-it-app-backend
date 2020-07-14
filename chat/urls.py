from django.contrib import admin
from django.urls import path
from chat import views

urlpatterns = [
    path("chat-users/", views.ChatUsersList.as_view(), name="chat",),
    path("test/", views.Test.as_view(), name="chat",),
]
