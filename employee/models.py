from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission
from django.core.validators import EmailValidator
from django.utils.timezone import now


class Employee(AbstractUser):
    class Meta:
        permissions = [
            ("can_add_product", "Can Add Product"),
            ("can_create_job_card", "Can Create Job Card"),
            ("can_edit_job_card", "Can Create Job Card"),
            ("can_edit_attendance", "Can Edit Attendance"),
        ]

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('mechanic', 'Mechanic'),
        ('accountant', 'Accountant'),
        ('helper', 'Helper'),
        ('sales', 'Sales'),
        ('finance', 'Finance'),
    ]

    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        error_messages={
            'unique': "A user with this email already exists.",
        }
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='helper')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    releving_date = models.DateField(blank=True, null=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    # readonly_fields = ('custom_permissions',)

    # def custom_permissions(self, obj):
    #     content_type = ContentType.objects.get_for_model(obj)
    #     permissions = Permission.objects.filter(content_type=content_type, codename__startswith='can_')
    #     return ', '.join([perm.name for perm in permissions])

    # custom_permissions.short_description = 'Custom Permissions'

    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'custom_permissions'),
    #     }),
    # )
    
    def save(self, *args, **kwargs):
        # user = super(Employee, self)
        # if(self.password):
        #     print(self.password, self.last_login)
        #     user.set_password(self.password)
        #     user.save()
        # else:
        #     user.save(update_fields=["last_login"])
        super().save(*args, **kwargs)

class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )
    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=(
            ("Present", "Present"),
            ("Absent", "Absent"),
            ("On Leave", "On Leave"),
        ),
        default="Absent"
    )

    class Meta:
        unique_together = ("employee", "date")  # Ensures one attendance record per employee per date

    def __str__(self):
        return f"{self.employee.first_name} - {self.date}"
    
class EmployeeShortLeave(models.Model):
    employee = models.ForeignKey(
        'Employee', 
        on_delete=models.CASCADE, 
        related_name="short_leaves"
    )
    date = models.DateField()  # The date of the short leave
    leave_start = models.TimeField()  # Start time of the short leave
    leave_end = models.TimeField(null=True, blank=True)  # End time of the short leave
    reason = models.TextField(blank=True, null=True)  # Optional reason for the leave
    approved = models.CharField(
        max_length=10,
        choices=(
            ("Approve", "Approve"),
            ("Pending", "Pending"),
            ("Rejected", "Rejected"),
        ),
        default="Pending"
    )    #models.BooleanField(default=False)  # Approval status for the leave

    class Meta:
        ordering = ['date', 'leave_start']
        verbose_name = "Employee Short Leave"
        verbose_name_plural = "Employee Short Leaves"