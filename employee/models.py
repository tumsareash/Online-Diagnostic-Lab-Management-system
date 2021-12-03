from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from datetime import datetime

# Create your models here.

class Employee(models.Model):
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)
    email = models.EmailField(unique= True)
    mobile = models.IntegerField()
    lab_id = 'lab202100012345A'
    password = models.CharField(max_length=10, unique=True)
    pic = models.FileField(upload_to='emp-pic',null=True,blank=True)

    def __str__(self):
        return self.fname + ' ' + self.lname


class Test(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    test_name = models.CharField(max_length=20)
    test_added_by = models.DateTimeField(auto_now_add=True)
    test_desc = models.TextField()
    test_rate = models.IntegerField()

    def __str__(self):
        return self.test_name
