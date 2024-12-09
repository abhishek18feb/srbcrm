from django.shortcuts import render
# import requests
from django.conf import settings


def indexpage(request):
    return render(request, 'index.html')

def homepage(request):
    return render(request, 'home.html')
