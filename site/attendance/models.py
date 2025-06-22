from django.db import models

class AttendanceRecord(models.Model):
    session_id = models.CharField(max_length=128)
    auditorium_id = models.CharField(max_length=128)
    counted_at = models.DateTimeField(auto_now_add=True)
    people_count = models.IntegerField()

    def __str__(self):
        return f'{self.auditorium_id} | {self.session_id} | {self.people_count} at {self.counted_at}'