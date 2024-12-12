from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee, EmployeeAttendance, EmployeeShortLeave
from datetime import date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

@login_required
def employee_short_leave_list(request):
    user = request.user
    today = date.today()
    if user.role == 'admin':
        leaveRequestData = EmployeeShortLeave.objects.all().order_by('date')
    else:
        leaveRequestData = EmployeeShortLeave.objects.filter(employee_id=user.id)
    # Paginate the queryset with 10 items per page
    page_number = request.GET.get('page')
    paginator = Paginator(leaveRequestData, 3)
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(page.num_pages)
    for leavedata in page:
        print(f"Title: {leavedata.date}, Author: {leavedata.leave_start}, Year: {leavedata.leave_end}, Year: {leavedata.reason}")
    return render(request, 'short_leave_list.html', {'page_title':"Short Leaves", "leaveRequestData": page, "page_number":page_number}) 

@require_POST
@login_required
def apply_short_leave(request):
    user = request.user
    today = date.today()
    if request.method == "POST":
        try:
            requestDate = request.POST.get('date')
            leaveStart = request.POST.get('leave_start')
            leaveEnd = request.POST.get('leave_end')
            reaSon = request.POST.get('reason')
            employeeShortLeaveObj = EmployeeShortLeave(date=requestDate, leave_start=leaveStart, leave_end=leaveEnd, reason=reaSon, employee_id=user.id)
            employeeShortLeaveObj.save()
            # Convert the object to a dictionary for JSON response
            response_data = {
                "id": employeeShortLeaveObj.id,
                "employee_id": employeeShortLeaveObj.employee_id,
                "leave_date": employeeShortLeaveObj.date,
                "leave_start": employeeShortLeaveObj.leave_start,
                "leave_end": employeeShortLeaveObj.leave_end,
                "leave_reason": employeeShortLeaveObj.reason,
            }
            print(response_data)
            # Return the saved object as JSON
            return JsonResponse({"status": "success", "data": response_data}, encoder=DjangoJSONEncoder, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)




