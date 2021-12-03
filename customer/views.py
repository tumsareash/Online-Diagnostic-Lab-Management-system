
import customer
from online_lab_management.settings import TEMPLATES
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
from employee import models
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 

# Create your views here.

def index(request):
    try:
        email = request.session['email']
        uid = Customer.objects.get(email=email)
        return render(request,'customer/cindex.html',{'uid':uid})
    except:
        return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def login(request):
     if request.method == "POST":
         try:
             uid = Customer.objects.get(email=request.POST['email'])
             
             if request.POST['password'] == uid.password:
                 request.session['email']=request.POST['email']
                 return render(request,'customer/cindex.html',{'uid':uid})
             else:
                 msg = 'Password does not match'
                 return render(request,'customer/login.html',{'msg':msg})
         except:
                msg = 'Email Not Registered. First Register yourself'
                return render(request,'customer/login.html',{'msg':msg})

     else:
         return render(request,'customer/login.html')


def register(request):
    if request.method == "POST":
        try:
            uid = Customer.objects.get(email=request.POST['email'])
            msg = 'Email aready exist'
            return render(request,'register.html',{'msg':msg})
        except:
            email = request.POST['email']
            global temp

            if request.POST['password'] == request.POST['cpassword']:
                temp = {
                    'fname' : request.POST['fname'],
                    'lname' : request.POST['lname'],
                    'email' : request.POST['email'],
                    'mobile' : request.POST['mobile'],
                    'address' : request.POST['address'],
                    'password' : request.POST['password']
                }
                otp = randrange(1000,9999)

                subject = 'Welcome to App '
                message = f'Hello {email}!! Your OTP is {otp}.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'customer/otp.html',{'otp':otp})

            else:
                msg = 'Password and Confirm Password does not matched'
                return render(request,'customer/register.html',{'msg':msg})


    else:
        return render(request,'customer/register.html')

def otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        uotp = request.POST['uotp']
        if otp == uotp:
            global temp
            Customer.objects.create(
                fname = temp['fname'],
                lname = temp['lname'],
                email = temp['email'],
                mobile = temp['mobile'],
                address = temp['address'],
                password = temp['password']
            )
            del temp
            msg = "Registered Successfully"
            return render(request,'customer/login.html',{'msg':msg})
        
        else:
            msg = 'OTP does not match'
            return render(request,'customer/otp.html',{'msg':msg,'otp':otp})
    else:
        return render(request,'customer/otp.html')

def forgot1(request):
    if request.method == 'POST':
        Email = request.POST['email']

        try:
            Customer.objects.get(email = Email)  
            otp = randrange(1000,9999)

            subject = 'Welcome to App '
            message = f'Hello {Email}!! Your OTP is {otp}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [Email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'customer/forgot2.html',{'otp':otp,'email':Email})
        
        except:
            msg = 'First Register yourself'
            return render(request,'customer/register.html',{'msg':msg})
    
    else:
        return render(request,'customer/forgot1.html')


def forgot2(request):
    if request.method == 'POST':
        Email = request.POST['email']
        otp = request.POST['otp']
        uotp = request.POST['uotp']

        if otp == uotp:
            return render(request,'customer/forgot3.html',{'email':Email})
        else:
            msg = 'OTP does not match'
            return render(request,'customer/forgot2.html',{'msg':msg,'email':Email,'otp':otp})
    
    else:
        return render(request,'customer/forgot2.html')

def forgot3(request):
    if request.method == 'POST':
        Email = request.POST['email']
        if request.POST['password'] == request.POST['cpassword']:
            uid = Customer.objects.get(email=Email)
            uid.password = request.POST['password']
            uid.save()
            msg = 'Password Updated successfully'
            return render(request,'customer/login.html',{'msg':msg})
        else:
            msg = 'Password and confirm password does not matched'
            return render(request,'customer/forgot3.html',{'email':Email,'msg':msg})
    else:
        return render(request,'customer/forgot3.html')

def profile(request):
    email = request.session['email']
    uid = Customer.objects.get(email=email)

    if request.method =="POST":
        
        uid.fname = request.POST['fname']
        uid.lname = request.POST['lname']
        uid.mobile = request.POST['mobile']
        uid.address = request.POST['address']
  
        if request.FILES:
            uid.pic = request.FILES['pic']
        uid.save()
        return render(request,'customer/cindex.html',{'uid':uid})

    else:
        return render(request,'customer/profile.html',{'uid':uid})

def logout(request):
    del request.session['email']
    msg = "Logout Successfully"
    return render(request,'index.html',{'msg':msg})
            
        
def view_test(request):
    tests = models.Test.objects.all()
    uid = Customer.objects.get(email=request.session['email'])
    return render(request,'customer/view-test.html',{'tests':tests,'uid':uid})


def booking(request,pk):
    uid = Customer.objects.get(email=request.session['email'])
    test = models.Test.objects.get(id=pk)
    return render(request,'customer/booking.html',{'test':test,'uid':uid})


def test_payment(request,pk):
    uid = Customer.objects.get(email=request.session['email'])
    global test
    test = models.Test.objects.get(id=pk)

    print(type(test))
    global amount
    currency = 'INR'
    amt = int(test.test_rate)  
    amount = amt*100 # convert rupees to paisa
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
    
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['uid'] = uid
    context['test'] = test

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@222")
    return render(request,'test-payment.html',context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        uid = Customer.objects.get(email=request.session['email'])
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                global amount, test
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    Appointment.objects.create(
                        customer = uid,
                        test = test,
                        amount = test.test_rate,
                        payment_id = payment_id,
                    )
                    del amount
                    del test
                    # render success page on successful caputre of payment
                    return render(request,'paymentsuccess.html',{'uid':uid})
                except:

                    # if there is an error while capturing payment.
                    return render(request,'paymentfail.html',{'uid':uid})
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html',{'uid':uid})
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()



def my_bookings(request):
    uid = Customer.objects.get(email=request.session['email'])
    appointments = Appointment.objects.all()
    return render(request,'my-bookings.html',{'uid':uid,'appointments':appointments})

def test_reports(request):
    uid = Customer.objects.get(email=request.session['email'])
    appointments = Appointment.objects.filter(customer = uid)
    return render(request,'customer/test-reports.html',{'uid':uid,'appointments':appointments})



