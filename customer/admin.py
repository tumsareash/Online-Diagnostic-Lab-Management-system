from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Customer)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer','test','amount','date','status']
