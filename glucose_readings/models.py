from django.db import models
from users.models import User

class GlucoseReading(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    value = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"User {self.user.name} - {self.value} at {self.timestamp}"
