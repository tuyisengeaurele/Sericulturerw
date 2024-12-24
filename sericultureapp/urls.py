from django.urls import path
from django.contrib.auth import views as auth_views
from sericultureapp.views import *

urlpatterns=[
    path('',display,name='Home'),
    path('login/',dlogin,name='login'),
    path('forgot password/',dforgot,name='forgot password'),
    path('register/',dregister, name='register'),
    path('about us/',dabout,name='about us'),
    path('services/',dservices,name='services'),
    path('admindashboard/',dadmin,name='admindashboard'),
    path('userdashboard/',duser,name='userdashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admindashboard/',dadmin, name='admindashboard'),
    path('user_management/',duser_management, name='user_management'),
    path('farm_management/',dfarm_management, name='farm_management'),
    path('production_management/',dproduction_management, name='production_management'),
    path('content_management/',dcontent_management, name='content_management'),
    path('analytics/',analytics, name='analytics'),
    path('admin_notifications/',admin_notifications, name='admin_notifications'),
    path('projects/',dprojects, name='projects'),
    path('contact_us/',dcontact, name='contact_us'),
    path('add_farm/',dadd_farm, name='add_farm'),
    path('feedback/',feedback, name='feedback'),
    path('submit_feedback/',submit_feedback, name='submit_feedback'),
    path('farm_details/',farm_details, name='farm_details'),
    path('farm_details1/',farm_details1, name='farm_details1'),
    path('farm_details2/',farm_details2, name='farm_details2'),
    path('my_farms/',my_farms, name='my_farms'),
    path('my_courses/',my_courses, name='my_courses'),
    path('user_feedback/',user_feedback, name='user_feedback'),
    path('user_notifications/',user_notifications, name='user_notifications'),
    path('userprofile/',userprofile, name='userprofile'),
    path('manage_staff/',manage_staff,name='manage_staff'),
    path('reports/',reports, name='reports'),
    path('add-farm/', add_farm, name='add_farm'),
    path('view_farm/',view_farm, name='view_farm'),
    path('farm_conditions/',farm_conditions, name='farm_conditions'),
    path('silkworm_batches/',silkworm_batches, name='silkworm_batches'),
    path('production/',production, name='production'),
    path('device_deployed/',device_deployed, name='device_deployed'),
    path('add_staff/',add_staff, name='add_staff'),
    path('pest_and_diseases/',pest_and_diseases, name='pest_and_diseases'),
    path('track_growth/',track_growth, name='track_growth'),
    path('feeding_schedule/',feeding_schedule, name='feeding_schedule'),
    path('community_chatroom/',community_chatroom, name='community_chatroom'),
    


    

]