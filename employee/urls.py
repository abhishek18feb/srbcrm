from django.urls import path
from . import views

urlpatterns = [
    # path('admin/users/<int:user_id>/password/', views.custom_user_password_change, name='custom_user_password_change'),
    path('login/', views.login_view, name='login'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
]