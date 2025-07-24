# chati/urls.py
from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.models import User 

urlpatterns = [
    path('', views.index, name='index'),
    path("feed", views.main, name='feed'),
    path("login", views.log_in, name='login'),
    path("logout", views.log_out, name='logout'),
    path("login/password_recover", views.recover_pass, name='password_recover'),
    path("login/password_recover/change_pass/<uidb64>/<token>/", 
         views.CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path("login/password_recover/change_pass/done", 
         views.CustomPasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
    path("signin", views.sign_in, name='signin'),
    path("chati/edit_profile/change_pass", views.change_pass, name='change_pass'),
    # path("login/password_recover/change_pass", views.change_pass),
    # path("chati/edit_profile/change_pass", views.change_pass),

    path("feed/post/<int:post_id>", views.post, name='post'),
    path("feed/chat-user/<int:chat_id>", views.chatting, name='chatting'),

     # Perfiles
     path("feed/profile/", views.own_profile, name='own-profile'),
     path("feed/profile/<str:username>/", views.profile, name='profile'),
     path("feed/profile/edit_user", views.edit_user, name="feed-profile-edit_user"),

    path("feed/chats", views.chats, name="feed-chat"),
    path("feed/chats/request", views.chat_request, name="feed-chat-request"),
    path("feed/chat-user", views.chatting, name="feed-chat-user"),
    path("feed/friends", views.friends, name="feed-friends"),
    path("feed/notifications", views.notification, name="feed-notifications"),

    # Publicaciones
    path("feed/post", views.post, name="feed-post"),  # Crear publicación
    # path("feed/post/<int:post_id>", views.view_post, name='post'),  # Ver publicación existente

    path("feed/post/comment", views.comment, name="feed-post-comment"),

    path('admin/', admin.site.urls),
]