from django.contrib import admin
from .models import Profile, Post, Comment, Friendship, Chat, Message, Settings

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Friendship)
admin.site.register(Chat)     
admin.site.register(Message) 
admin.site.register(Settings)