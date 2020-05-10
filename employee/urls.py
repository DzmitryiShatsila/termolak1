from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile-view'),
    path('user/update/', views.profile_update, name='profile-update'),
    path('user/change_password/', views.change_password, name='change-pass'),
    path('all_employees/', views.AllEmployees.as_view(), name='all-employees'),
    path('<slug:slug>/employee_detail/', views.EmployeeDetail.as_view(), name='employee-detail'),
    path('create_employee/', views.crate_employee, name='employee-create'),
    path('<str:username>/delete_employee', views.delete_employee, name='employee-delete'),

]