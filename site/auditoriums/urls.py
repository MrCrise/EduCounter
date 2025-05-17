from django.urls import path
from . import views

app_name = 'auditoriums'

urlpatterns = [
    path('', views.auditoriums_list, name='auditoriums_list'),
    path('<str:auditorium_name>/',
         views.auditorium_detail,
         name='auditorium_detail'),
]
