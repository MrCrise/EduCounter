from django.urls import path
from .views import save_attendance

app_name = 'attendance'

urlpatterns = [
    path('save-attendance/', save_attendance, name='save_attendance'),
]