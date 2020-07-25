from django.contrib import admin
from django.urls import path
from chat import views

urlpatterns = [
    path("chat-history/", views.MessageList.as_view(), name="chat",),
    path("user-list/", views.UserList.as_view(), name="chat",),
]
