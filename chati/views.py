from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
	return HttpResponse("¡Hola Mundo desde Django!")


def index(request):
    return render(request, "chati/LandingPage.html")
# Create your views here.
