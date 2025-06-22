from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Auditorium(models.Model):
    name = models.CharField(max_length=10, unique=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # преподаватель
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    teacher = models.CharField(max_length=255)
    students_count = models.IntegerField()
    student_list = models.TextField()
    module = models.CharField(max_length=100, blank=True, null=True)
    people_count = models.IntegerField(blank=True, null=True)
    updated_at = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.subject} in {self.auditorium} by {self.teacher}"