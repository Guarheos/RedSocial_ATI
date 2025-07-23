from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Profile, Post, Comment, Friendship, Chat, Message

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



def index(request):
	return render(request, "chati/LandingPage.html")

def log_in(request):
	return render(request, "chati/LogIn.html")

def sign_in(request):
	return render(request, "chati/SignIn.html")

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