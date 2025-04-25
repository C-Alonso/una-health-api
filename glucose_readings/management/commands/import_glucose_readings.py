import os
import pandas as pd
from django.core.management.base import BaseCommand
from glucose_readings.models import GlucoseReading
from django.contrib.auth.models import User
from datetime import datetime

GLUCOSE_READING_TIMESTAMP = 'Gerätezeitstempel'
GLUCOSE_READING_VALUE = 'Glukosewert-Verlauf mg/dL'


class Command(BaseCommand):
    help = 'Import glucose readings from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Directory containing the CSV files')

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']

        if not os.path.isdir(directory):
            self.stderr.write(f"Directory not found: {directory}")
            return

        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                try:
                    user_id = int(filename.split('_')[1].split('.')[0])  # user_1.csv → 1
                    user = User.objects.get(pk=user_id)
                except (IndexError, ValueError, User.DoesNotExist) as e:
                    self.stderr.write(f"Skipping file {filename}: {e}")
                    continue

                path = os.path.join(directory, filename)
                df = pd.read_csv(path, skiprows=1)
                df_selected = df[[GLUCOSE_READING_TIMESTAMP, GLUCOSE_READING_VALUE]]

                for _, row in df_selected.iterrows():
                    try:
                        timestamp = datetime.strptime(row[GLUCOSE_READING_TIMESTAMP], "%d-%m-%Y %H:%M")
                        value = int(row[GLUCOSE_READING_VALUE])

                        GlucoseReading.objects.create(
                            user=user,
                            glucose_level=value,
                            # ToDo: address warning  DateTimeField GlucoseReading.reading_datetime received a naive datetime (2021-02-18 10:42:00) while time zone support is active.
                            reading_datetime=timestamp
                        )
                    except Exception as e:
                        self.stderr.write(f"Error in {filename}: {e}")
                        continue

                self.stdout.write(self.style.SUCCESS(f"Successfully imported {filename}"))
