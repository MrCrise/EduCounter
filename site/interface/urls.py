from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('auditoriums/', views.auditoriums, name='auditoriums'),
    path('auditorium/<str:auditorium_name>/', views.auditorium_detail, name='auditorium_detail'),
    path('logout/', views.logout, name='logout'),
]