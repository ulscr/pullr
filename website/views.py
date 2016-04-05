from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from website.models import Ringer,Performance

from . import tasks

# Create your views here.

def index(request):
    ringers = Ringer.objects.order_by("name");

    performances = Performance.objects.order_by("method");

    return render(request, 'website/index.html', {'ringers': ringers, 'performances': performances})

def import_names(request):
    if ('name' in request.POST.keys()):
      tasks.query_bellboard(request.POST['name'])
      return render(request, 'website/import.html', {'message':"Imported for " + request.POST['name']});
    return render(request, 'website/import.html')
