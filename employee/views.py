
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
from customer import models

# Create your views here.

def emp_index(request):
    return render(request,'emp-index.html')

def emp_login(request):
    if request.method == 'POST':
        try:
            uid = Employee.objects.get(email = request.POST['email'])

            if request.POST['password'] == uid.password:
                global appointments
                request.session['email']=request.POST['email']
                appointments = models.Appointment.objects.all()
                return render(request,'emp-dashboard.html',{'uid':uid,'appointments':appointments})
            else:
                msg = 'Incorrect Password'
                return render(request,'emp-login.html',{'msg':msg})

        except:
            msg = 'First register yourself'
            return render(request,'emp-login.html',{'msg':msg})

    else:
        return render(request,'emp-login.html')

def emp_logout(request):
    del request.session['email']
    msg = "Logout Successfully"
    return render(request,'emp-login.html',{'msg':msg})


def emp_register(request):
    
    if request.method == 'POST':
       
        try:
            uid = Employee.objects.get(email=request.POST['email'])
            msg = "Employee already registered"
            return render(request,'emp-login.html',{'msg':msg})
        except:
            
            if request.POST['lab_id'] == 'lab202100012345A':

                if request.POST['password'] == request.POST['cpassword']:
                    global temp
                    temp = {
                    'fname' : request.POST['fname'],
                    'lname' : request.POST['lname'],
                    'email' : request.POST['email'],
                    'mobile' : request.POST['mobile'],
                    'password' : request.POST['password'] 
                    }

                    otp = randrange(1000,9999)

                    subject = 'Welcome to App '
                    message = f'Hello Employee!! Your OTP is {otp}.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.POST["email"], ]
                    send_mail( subject, message, email_from, recipient_list )
                    return render(request,'emp-otp.html',{'otp':otp})
                
                else:
                    msg = "Password & Confirm Password not match"
                    return render(request,'emp-register.html',{'msg':msg})

            else:
                msg = "Irrevalent lab ID"
                return render(request,'emp-register',{'msg':msg})
    else:
        return render(request,'emp-register.html')


def emp_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        uotp = request.POST['uotp']

        if otp == uotp:
            global temp
            Employee.objects.create(
                fname = temp['fname'],
                lname = temp['lname'],
                email = temp['email'],
                mobile = temp['mobile'],
                password = temp['password']
            )
            if temp:
                del temp
            
            msg = "Employee Registered Successfully"
            return render(request,'emp-login.html',{'msg':msg})

        else:
            msg = 'OTP does not match'
            return render(request,'emp-otp.html',{'otp':otp,'msg':msg})
    
    else:
        return render(request,'emp-otp')

   
def emp_dashboard(request):
    uid = Employee.objects.get(email=request.session['email'])
    global appointments
    appointments = models.Appointment.objects.all()
    total_bookings = len(appointments)
    x=0
    y=0
    z=0
    for appointment in appointments:
        if appointment.status == 'Live':
            x = x + 1
        elif appointment.status == 'Sample Collected':
            y = y + 1
        else:
            z = z + 1   
    
    return render(request,'emp-dashboard.html',{'appointments':appointments,'uid':uid,'total_bookings':total_bookings,"live_bookings":x,"sample_collected_bookings":y,"done_bookings":z})


def emp_forgot1(request):
    if request.POST:
        email = request.POST['email']

        try:
            Employee.objects.get(email=email)
            otp = randrange(1000,9999)

            subject = 'Welcome to App '
            message = f'Hello {email}!! Your OTP is {otp}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'emp-forgot2.html',{'otp':otp,'email':email})

        except:
            msg = 'First Register yourself'
            return render(request,'emp-register.html',{'msg':msg})

    else:
        return render(request,'emp-forgot1.html')


def emp_forgot2(request):
    if request.method == 'POST':
        Email = request.POST['email']
        otp = request.POST['otp']
        uotp = request.POST['uotp']

        if otp == uotp:
            return render(request,'emp-forgot3.html',{'email':Email})
        else:
            msg = 'OTP does not match'
            return render(request,'emp-forgot2.html',{'msg':msg,'email':Email,'otp':otp})
    
    else:
        return render(request,'emp-forgot2.html')

def emp_forgot3(request):
    if request.method == 'POST':
        Email = request.POST['email']
        if request.POST['password'] == request.POST['cpassword']:
            user = Employee.objects.get(email=Email)
            user.password = request.POST['password']
            user.save()
            msg = 'Password Updated successfully'
            return render(request,'emp-login.html',{'msg':msg})
        else:
            msg = 'Password and confirm password does not matched'
            return render(request,'emp-forgot3.html',{'email':Email,'msg':msg})
    else:
        return render(request,'emp-forgot3.html')

def emp_profile(request):
    uid = Employee.objects.get(email=request.session['email'])
    
    if request.POST:
        uid.fname = request.POST['fname']
        uid.lname = request.POST['lname']
        uid.mobile = request.POST['mobile']

        if request.FILES:
            uid.pic = request.FILES['pic']
        
        uid.save()
        msg = "Data Updated Successfully"
        return render(request,'emp-profile.html',{'msg':msg,'uid':uid})

    else:
        return render(request,'emp-profile.html',{'uid':uid})
  

def emp_add_test(request):
    uid = Employee.objects.get(email=request.session['email'])
    if request.method == 'POST':
        
        Test.objects.create(
            employee = uid,
            test_name = request.POST['test_name'],
            test_desc = request.POST['test_desc'],
            test_rate = request.POST['test_rate']      
            )
        msg = "Test added successfully"
        return render(request,'emp-add-test.html',{'uid':uid,'msg':msg})

    else:
        return render(request,'emp-add-test.html',{'uid':uid})


def emp_view_test(request):
    uid = Employee.objects.get(email=request.session['email'])
    tests = Test.objects.all()
    return render(request,'emp-view-test.html',{'uid':uid,'tests':tests})
        
def emp_delete_test(request,pk):
    uid = Employee.objects.get(email=request.session['email'])
    test = Test.objects.get(id=pk)
    test.delete()
    return redirect('emp-view-test')

def emp_edit_test(request,pk):
    uid = Employee.objects.get(email=request.session['email'])
    test = Test.objects.get(id=pk)

    if request.method == "POST":
        test.test_name = request.POST['test_name']
        test.test_desc = request.POST['test_desc']
        test.test_rate = request.POST['test_rate']
        test.save()
        msg = "Test Edited Successfully"
        return redirect('emp-view-test')

    else:
        return render(request,'emp-edit-test.html',{'test': test,'uid':uid})


def emp_all_bookings(request):
    uid = Employee.objects.get(email= request.session['email']) 
    appointments = models.Appointment.objects.all()
    return render(request,'emp-all-bookings.html',{'uid':uid,'appointments':appointments})


def change_status(request,pk):
    uid = Employee.objects.get(email=request.session['email'])
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = 'Sample Collected'
    appointment.save()
    appointments = models.Appointment.objects.all()
    return render(request,'emp-all-bookings.html',{'appointments':appointments,'uid':uid})

def update_report(request):
    uid = Employee.objects.get(email=request.session['email'])
    appointments = models.Appointment.objects.filter(status='Sample Collected')
    return render(request,'update-report.html',{'appointments':appointments,'uid':uid})   
    

def upload_result(request,pk):
    appointment = models.Appointment.objects.get(id=pk)
    uid = Employee.objects.get(email=request.session['email'])
  
    if request.method == "POST":
        appointment.test_result = request.FILES['test_result']
        appointment.status = "Done"
        appointment.save()
        msg = "Test Report Updated Successfully"
        appointments = models.Appointment.objects.all()
        return render(request,'update-report.html',{'msg':msg,'appointments':appointments,'uid':uid})
        

def all_reports(request):
    uid = Employee.objects.get(email=request.session['email'])
    appointments = models.Appointment.objects.filter(status = 'Done')
    return render(request,'all-reports.html',{'appointments':appointments,'uid':uid})
    
        
