# Generated by Django 5.1.4 on 2024-12-09 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0002_employee_hire_date_employee_phone_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="hire_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="releving_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]