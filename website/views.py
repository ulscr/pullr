from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from . import tasks

# Create your views here.

def index(request):
    rendered = render_to_string('website/index.html')

    return HttpResponse(rendered);

def test(request, stuff):
    tasks.query_bellboard(stuff)
    return HttpResponse("Hello " + stuff);
