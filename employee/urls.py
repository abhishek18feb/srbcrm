from django.urls import path
from . import views

urlpatterns = [
    # path('admin/users/<int:user_id>/password/', views.custom_user_password_change, name='custom_user_password_change'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout_confirmation'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('short-leave-list/', views.employee_short_leave_list, name='employee_short_leave_list'),
    path('apply-short-leave/', views.apply_short_leave, name='apply_short_leave'),
]