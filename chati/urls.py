# chati/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.log_in),
    path("login/password_recover", views.recover_pass),
    path("signin", views.sign_in),
    path("login/password_recover/change_pass", views.change_pass),
    path("chati/edit_profile/change_pass", views.change_pass),
    path("chatrequest", views.chat_request),

    path("chati", views.main),
    path("chati/chats", views.chats),
    path("chati/chats/requests", views.chat_request),
    path("chati/chat-user", views.chatting),
    path("chati/friends", views.friends),
    path("chati/profile", views.profile),
    path("chati/profile/edit_user", views.edit_user),
    path("chati/notifications", views.notification),
    path("chati/post", views.post),
]