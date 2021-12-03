from django.urls import path
from .import views
from django.contrib import admin


urlpatterns = [
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    path('login/',views.login, name='login'),
    path('register/',views.register, name='register'),
    path('otp/',views.otp,name='otp'),
    path('forgot1/',views.forgot1,name='forgot1'),
    path('forgot2/',views.forgot2,name='forgot2'),
    path('forgot3/',views.forgot3,name='forgot3'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('view-test/',views.view_test,name='view-test'),
    path('booking/<int:pk>',views.booking,name='booking'),
    path('test-payment/<int:pk>',views.test_payment,name='test-payment'),
    path('test-payment/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('my-bookings/',views.my_bookings,name='my-bookings'),
    path('test-reports/',views.test_reports,name='test-reports'),
    
    
]
