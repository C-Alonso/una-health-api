# glucose_readings/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from glucose_readings.models import GlucoseReading
from datetime import datetime


class GlucoseReadingModelTest(TestCase):

    def setUp(self):
        """Create a user to associate glucose readings."""
        self.user = User.objects.create(username="John", email="john@example.com")

    def test_glucose_reading_creation(self):
        """Test the creation of a glucose reading."""
        glucose_reading = GlucoseReading.objects.create(
            user=self.user,
            glucose_level=120,
            reading_datetime=datetime(2025, 4, 25, 10, 30)
        )

        # Check if the reading is correctly saved
        self.assertEqual(glucose_reading.user, self.user)
        self.assertEqual(glucose_reading.glucose_level, 120)
        self.assertEqual(glucose_reading.reading_datetime, datetime(2025, 4, 25, 10, 30))

    def test_str_method(self):
        """Test the string representation of the glucose reading."""
        glucose_reading = GlucoseReading.objects.create(
            user=self.user,
            glucose_level=150,
            reading_datetime=datetime(2025, 4, 25, 12, 45)
        )

        self.assertEqual(str(glucose_reading), "User John - 150 at 2025-04-25 12:45:00")
