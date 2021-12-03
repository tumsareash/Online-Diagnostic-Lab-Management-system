from django.urls import path
from .import views

urlpatterns = [
    path('',views.emp_index,name='emp-index'),
    path('emp-login/',views.emp_login,name='emp-login'),
    path('emp-register/',views.emp_register,name='emp-register'),
    path('emp-otp/',views.emp_otp,name='emp-otp'),
    path('emp-dashboard/',views.emp_dashboard,name='emp-dashboard'),
    path('emp-logout/',views.emp_logout,name='emp-logout'),
    path('emp-add-test/',views.emp_add_test,name='emp-add-test'),
    path('emp-view-test/',views.emp_view_test,name='emp-view-test'),
    path('emp-delete-test/<int:pk>',views.emp_delete_test,name='emp-delete-test'),
    path('emp-edit-test/<int:pk>',views.emp_edit_test,name='emp-edit-test'),
    path('emp-forgot1/',views.emp_forgot1,name="emp-forgot1"),
    path('emp-forgot2/',views.emp_forgot2,name="emp-forgot2"),
    path('emp-forgot3/',views.emp_forgot3,name="emp-forgot3"),
    path('emp-profile/',views.emp_profile,name="emp-profile"),
    path('emp-all-bookings/',views.emp_all_bookings,name="emp-all-bookings"),
    path('change-status/<int:pk>',views.change_status,name="change-status"),
    path('update-report/',views.update_report,name='update-report'),
    path('upload-result/<int:pk>',views.upload_result,name='upload-result'),
    path('all-reports',views.all_reports,name='all-reports'),
    
]
