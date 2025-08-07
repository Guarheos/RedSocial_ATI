from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Profile, Post, Settings
from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm,
    ProfileEditForm,
    PostForm
)

class UserModelTests(TestCase):
    def test_signal_creates_settings_for_new_user(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertTrue(Settings.objects.filter(user=user).exists())
        self.assertEqual(Settings.objects.filter(user=user).count(), 1)
        settings = Settings.objects.get(user=user)
        self.assertEqual(settings.profile_visibility, 'public')

class AuthFormTests(TestCase):
    def test_user_creation_form_valid(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_user_creation_form_invalid(self):
        # Test mismatched passwords
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'invalid-email',
            'password1': 'password1',
            'password2': 'password2'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('email', form.errors)

    def test_authentication_form_valid(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        form_data = {'username': 'testuser', 'password': 'testpass'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_authentication_form_invalid(self):
        form_data = {'username': 'nonexistent', 'password': 'wrong'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, bio="Test bio")

    def test_profile_creation(self):
        self.assertEqual(str(self.profile), 'testuser')
        self.assertEqual(self.profile.bio, "Test bio")
        self.assertEqual(self.profile.user, self.user)

class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            user=self.user, 
            text_content="Test post content"
        )

    def test_post_creation(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.text_content, "Test post content")
        self.assertIsNotNone(self.post.post_date)

class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass', 
            email='test@example.com'
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chati/LogIn.html')
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertRedirects(response, reverse('feed'))

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario o contraseña inválidos")

    def test_signup_view_get(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chati/SignIn.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_signup_view_post_valid(self):
        response = self.client.post(reverse('signin'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!'
        })
        self.assertRedirects(response, reverse('feed'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='newuser').exists())

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, bio="Original bio")
        self.client.login(username='testuser', password='testpass')

    def test_own_profile_view(self):
        response = self.client.get(reverse('own-profile'))
        self.assertRedirects(response, reverse('profile', kwargs={'username': 'testuser'}))

    def test_profile_view(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chati/ProfileUser.html')
        self.assertEqual(response.context['profile'], self.profile)
        self.assertTrue(response.context['is_own_profile'])

    def test_edit_profile_get(self):
        response = self.client.get(reverse('feed-profile-edit_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chati/EditProfile.html')
        self.assertIsInstance(response.context['form'], ProfileEditForm)

    def test_edit_profile_post(self):
        response = self.client.post(reverse('feed-profile-edit_user'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'updateduser',
            'email': 'updated@example.com',
            'bio': 'Updated bio',
            'profile_visibility': 'private'
        })
        self.assertRedirects(response, reverse('profile', kwargs={'username': 'updateduser'}))
        
        # Refresh objects from DB
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        
        # Get settings via signal-created instance
        settings = self.user.settings
        
        # Verify updates
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(settings.profile_visibility, 'private')

class PostViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_post_creation_get(self):
        response = self.client.get(reverse('feed-post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chati/Publication.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_creation_post(self):
        response = self.client.post(reverse('feed-post'), {
            'text_content': 'New test post content'
        })
        self.assertRedirects(response, reverse('feed'))
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.text_content, 'New test post content')
        self.assertEqual(post.user, self.user)

class SearchViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)

    def test_user_search(self):
        response = self.client.get(reverse('buscar_usuarios'), {'q': 'user'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['username'], 'user1')
        self.assertEqual(data[1]['username'], 'user2')

    def test_user_search_specific(self):
        response = self.client.get(reverse('buscar_usuarios'), {'q': 'user1'})
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['username'], 'user1')