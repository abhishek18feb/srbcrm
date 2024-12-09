from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee
# Create your views here.

@csrf_protect
def login_view(request):
    if request.method == "POST":
        username = request.POST['email']  # Use email as username
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

@login_required
def mark_attendance(request):
    if request.method == "POST":
        pass

    return render(request, 'attendance.html') 

