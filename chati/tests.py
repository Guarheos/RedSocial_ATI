from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .models import Profile, Post, Comment, Friendship, Chat, Message, Settings


class UserModelTests(TestCase):
    def test_signal_crea_settings_para_nuevo_usuario(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertTrue(Settings.objects.filter(user=user).exists())
        self.assertEqual(Settings.objects.filter(user=user).count(), 1)
        settings = Settings.objects.get(user=user)
        self.assertEqual(settings.profile_visibility, 'public')


class SocialModelsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='usuario1', password='pw1')
        self.user2 = User.objects.create_user(username='usuario2', password='pw2')
        self.profile1 = Profile.objects.create(user=self.user1, bio="Biografía de prueba")
        self.post1 = Post.objects.create(user=self.user1, text_content="Este es un post de prueba.")

    def test_creacion_de_perfil(self):
        self.assertEqual(str(self.profile1), 'usuario1')
        self.assertEqual(self.profile1.bio, "Biografía de prueba")
        self.assertEqual(self.profile1.user, self.user1)

    def test_creacion_de_post(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post1.user, self.user1)
        self.assertEqual(self.post1.text_content, "Este es un post de prueba.")
        self.assertEqual(str(self.post1), f'Post de usuario1 - {self.post1.id}')

    def test_solicitud_de_amistad(self):
        friendship = Friendship.objects.create(requester=self.user1, receiver=self.user2)
        self.assertEqual(friendship.status, 'pending') # Probar el valor por defecto
        self.assertEqual(str(friendship), 'usuario1 to usuario2 - pending')

    def test_restriccion_unique_together_en_amistad(self):
        Friendship.objects.create(requester=self.user1, receiver=self.user2)
        # Intentar crear la misma relación debe lanzar un IntegrityError
        with self.assertRaises(IntegrityError):
            Friendship.objects.create(requester=self.user1, receiver=self.user2)
