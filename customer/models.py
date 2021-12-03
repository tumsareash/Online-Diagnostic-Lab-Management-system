from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from employee.models import *   


# Create your models here.

class Customer(models.Model):
    
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=14)
    password = models.CharField(max_length=15)
    address = models.TextField()
    pic = models.FileField(upload_to='profile',null=True,blank=True,default='avtar.png')

    def __str__(self):
        return self.email

class Appointment(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default='Live')
    payment_id = models.CharField(max_length=50,default='')
    test_result = models.FileField(upload_to='test_report',null=True,blank=True)

    def __str__(self):
        return self.customer.email + " ==>> " + str(self.date)

