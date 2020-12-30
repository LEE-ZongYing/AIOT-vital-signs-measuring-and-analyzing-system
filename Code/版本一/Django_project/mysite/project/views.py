from django.shortcuts import render
from django.http import HttpResponse
from .models import Iccard
from datetime import datetime

def hello_world(request):
    people = Iccard.objects.all()
    return render(request,'hello_word.html',locals())
# Create your views here.

