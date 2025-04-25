from rest_framework import serializers
from glucose_readings.models import GlucoseReading

class GlucoseReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseReading
        fields = ['id', 'user', 'glucose_level', 'reading_datetime']
