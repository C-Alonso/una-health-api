from django.db import models
from django.contrib.auth.models import User

class GlucoseReading(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    glucose_level = models.IntegerField()
    reading_datetime = models.DateTimeField()

    def __str__(self):
        return f"User {self.user.username} - {self.glucose_level} at {self.reading_datetime}"
