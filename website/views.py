from django.shortcuts import render
from django.http import HttpResponse

from . import tasks

# Create your views here.

def index(request):
    return HttpResponse("Hello World!")

def test(request, stuff):
    tasks.query_bellboard(stuff)
    return HttpResponse("Hello " + stuff);
