from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from .models import Profile, Post, Comment, Friendship, Chat, Message
from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    ProfileEditForm
)

# Manejo de formas
def index(request):
    return render(request, "chati/LandingPage.html")

def log_in(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
        messages.error(request, "Usuario o contraseña inválidos")
    else:
        form = CustomAuthenticationForm()
    return render(request, "chati/LogIn.html", {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil automáticamente
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('feed')
    else:
        form = CustomUserCreationForm()
    return render(request, "chati/SignIn.html", {'form': form})

def recover_pass(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='chati/password_reset_email.html',
                subject_template_name='chati/password_reset_subject.txt'
            )
            messages.success(request, "Se han enviado instrucciones a tu correo para restablecer tu contraseña")
            return redirect('login')
    else:
        form = CustomPasswordResetForm()
    return render(request, "chati/RecoverPass.html", {'form': form})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = "chati/ChangePass.html"
    
    def form_valid(self, form):
        messages.success(self.request, "Tu contraseña ha sido restablecida exitosamente")
        return super().form_valid(form)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "chati/PasswordResetComplete.html"

@login_required
def change_pass(request):
    if request.method == 'POST':
        form = CustomSetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu contraseña ha sido cambiada exitosamente")
            return redirect('profile')
    else:
        form = CustomSetPasswordForm(request.user)
    return render(request, "chati/ChangePass.html", {'form': form})

@login_required
def edit_user(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, "chati/EditProfile.html", {'form': form})

 
# Metodos de renderizados dinamico

def main(request):
    posts = Post.objects.all().order_by('-post_date')
    return render(request, "chati/MainPage.html", {'posts': posts})

def profile(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    return render(request, "chati/ProfileUser.html", {'profile': user_profile})

def friends(request):
    friendships = Friendship.objects.filter(
        Q(requester=request.user) | Q(receiver=request.user),
        status='accepted'
    )
    return render(request, "chati/Friends.html", {'friendships': friendships})

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('comment_date')
    return render(request, "chati/Publication.html", {'post': post, 'comments': comments})

def chatting(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('sent_date')
    return render(request, "chati/ChattingUser.html", {'chat': chat, 'messages': messages})

# Renderizado estatico
def index(request):
	return render(request, "chati/LandingPage.html")

def change_pass(request):
	return render(request, "chati/ChangePass.html")

def chat_request(request):
	return render(request, "chati/ChatRequests.html")

def chats(request):
	return render(request, "chati/Chats.html")

def chatting(request):
	return render(request, "chati/ChattingUser.html")

def comment(request):
	return render(request, "chati/Comments.html")

def edit_user(request):
	return render(request, "chati/EditProfile.html")

def friends(request):
	return render(request, "chati/Friends.html")

def main(request):
	return render(request, "chati/MainPage.html")

def notification(request):
	return render(request, "chati/Notifications.html")

def profile(request):
	return render(request, "chati/ProfileUser.html")

def post(request):
	return render(request, "chati/Publication.html")

def recover_pass(request):
	return render(request, "chati/RecoverPass.html")

@login_required
def log_out(request):
    logout(request)
    return redirect('index')