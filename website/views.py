from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from website.models import Ringer,Performance

from . import tasks

# Create your views here.

def index(request):
    ringers = Ringer.objects.order_by("name");

    performances = Performance.objects.order_by("method");

    rendered = render_to_string('website/index.html', {'ringers': ringers, 'performances': performances})

    return HttpResponse(rendered);

def test(request, stuff):
    tasks.query_bellboard(stuff)
    return HttpResponse("Hello " + stuff);
