from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	return render(request, "chati/LandingPage.html")

def log_in(request):
	return render(request, "chati/LogIn.html")

def sign_in(request):
	return render(request, "chati/SignIn.html")

def change_pass(request):
	return render(request, "chati/ChangePass.html")

def chat_request(request):
	return render(request, "chati/ChatRquests.html")

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