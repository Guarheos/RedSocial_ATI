from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_content = models.TextField()
    media_url = models.URLField(max_length=200, blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post de {self.user.username} - {self.id}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.user.username} en el post {self.post.id}'

class Friendship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptada'),
        ('declined', 'Rechazada'),
    ]
    requester = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('requester', 'receiver')

    def __str__(self):
        return f'{self.requester} to {self.receiver} - {self.status}'

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat entre {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message_content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.sender.username} en chat {self.chat.id}'

class Settings(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Público'),
        ('private', 'Privado'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES, default='public')

    def __str__(self):
        return f'Configuración de {self.user.username}'