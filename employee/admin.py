from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Employee
# from django import forms
# Register your models here.
from .forms import EmployeeRegister
from django.contrib.auth.hashers import make_password


class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeRegister
    site_header = "Custom Admin Panel"
    site_title = "Custom Admin Portal"
    index_title = "Welcome to the Admin Panel"
    list_display = ('first_name', 'last_name', 'username', 'email', 'role')  # Only these fields will appear
    search_fields = ('first_name', 'last_name', 'username', 'email', 'role')

    def get_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            exclude = ('password',)  # Exclude the password field
            return ('first_name', 'last_name', 'username', 'email',  'user_permissions', 'role', 'hire_date', 'releving_date', 'phone_number')  # Hide 'secret_field'
        else:  # Adding a new object
            return ('first_name', 'last_name', 'username', 'password', 'email', 'user_permissions', 'role', 'hire_date', 'releving_date', 'phone_number')

    def save_model(self, request, obj, form, change):
        # Check if the password has been updated
        if 'password' in form.changed_data:
            # Hash the password only if it's not already hashed
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Employee, EmployeeAdmin)
# admin.site.unregister(Employee)
# admin.site.register(Employee, EmployeeAdmin)

