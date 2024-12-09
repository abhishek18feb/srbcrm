from django import forms
from .models import Employee
from django.forms import DateInput

class EmployeeRegister(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'hire_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'releving_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }

    first_name = forms.CharField(max_length=150, label='First Name')
    last_name = forms.CharField(max_length=150, label='Last Name')
    username = forms.CharField(max_length=150, label='Unique User Name')
    email = forms.CharField(max_length=150, label='Email')
    phone_number = forms.CharField(max_length=150, label='Phone Number')
    # hire_date = forms.DateField(required=True)
    # releving_date = forms.CharField(required=False)

    # role = forms.CharField(max_length=150, label='Role')
    password = forms.CharField(
        max_length=128,
        label='Password',
        widget=forms.PasswordInput,
        required=False,  # Optional to allow editing without forcing a password change
        help_text="Leave blank to keep the current password."
    )

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'username', 'password', 'email',  'role']