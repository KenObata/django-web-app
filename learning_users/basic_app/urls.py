from django.contrib import admin
from basic_app import views
from django.urls import path

#template
app_name="basic_app"

urlpatterns = [
               path('register/',views.register,name='register'),
               path('user_login',views.user_login,name='user_login'),
]
