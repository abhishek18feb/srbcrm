from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee, EmployeeAttendance
from datetime import date
# Create your views here.

LOGIN_REDIRECT_URL='employee/login'

@csrf_protect
def login_view(request):
    if request.method == "POST":
        username = request.POST['email']  # Use email as username
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            
            login(request, user)
            return redirect('/employee/mark-attendance/')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

@login_required
def mark_attendance(request):
    user = request.user
    today = date.today()
    
    attendanceData = EmployeeAttendance.objects.filter(employee_id=request.user.id, date=today).first()
    
    if request.method == "POST":
        print(request.POST)
        if attendanceData==None:
            check_in_time = request.POST.get('check_in_time')
            
            employee_id=request.user.id
            empattendanceobj = EmployeeAttendance(employee_id=employee_id, date = today, check_in_time=check_in_time, status='Present')
            empattendanceobj.save()
            attendanceData = empattendanceobj
        else:
            attendanceData.check_out_time = request.POST.get('check_out_time')
            attendanceData.save()
    print(request.user.username, request.user.email, request.user.id, today)
    print(f"Attendance Data {attendanceData}")
    return render(request, 'attendance.html', {'user':user, 'attendanceData':attendanceData}) 

