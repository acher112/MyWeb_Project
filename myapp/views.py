from django.contrib import admin
from django.http import HttpResponse

def home(request):
    return HttpResponse("hi hello")

def contact(request):
    return HttpResponse("My ROOM")