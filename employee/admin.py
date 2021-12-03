from django.contrib import admin

from employee.models import Employee, Test

# Register your models here.

admin.site.register(Employee)
admin.site.register(Test)