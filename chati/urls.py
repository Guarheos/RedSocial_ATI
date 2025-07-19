# chati/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('inicio', views.index, name='index'),
    path("login", views.log_in),
    path("login/password_recover", views.recover_pass),
    path("signin", views.sign_in),
    path("login/password_recover/change_pass", views.change_pass),
    path("chati/edit_profile/change_pass", views.change_pass),

    path("feed", views.main),
    path("feed/chats", views.chats),
    path("feed/chats/request", views.chat_request),
    path("feed/chat-user", views.chatting),
    path("feed/friends", views.friends),
    path("feed/profile", views.profile),
    path("feed/profile/edit_user", views.edit_user),
    path("feed/notifications", views.notification),
    path("feed/post", views.post),
    path("feed/post/comment", views.profile),
]