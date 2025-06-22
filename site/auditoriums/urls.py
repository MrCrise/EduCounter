from django.urls import path
from . import views

app_name = 'auditoriums'

urlpatterns = [
    path('', views.auditoriums_list, name='auditoriums_list'),
    path('charts/', views.auditorium_charts, name='charts'),
    path('charts/<int:auditorium_id>/', views.auditorium_chart_data, name='chart_data'),
    path('<str:auditorium_name>/', views.auditorium_detail, name='auditorium_detail'),
]