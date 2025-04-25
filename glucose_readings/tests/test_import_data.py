from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import User
from glucose_readings.models import GlucoseReading
from io import StringIO
import os
import tempfile


class CommandTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_2 = User.objects.create_user(username='testuser_2', password='testpassword_2')

        # Create a temporary directory to simulate file imports
        self.test_dir = tempfile.mkdtemp()

        # Create sample CSV files in the directory
        self.create_sample_csv('user_1.csv', self.user.id)
        self.create_sample_csv('user_2.csv', self.user_2.id)

    def create_sample_csv(self, filename, user_id):
        csv_data = "Glukose-Werte,Erstellt am,24-02-2021 12:12 UTC,Erstellt von,bbb\n"
        csv_data += "Gerät,Seriennummer,Gerätezeitstempel,Aufzeichnungstyp,Glukosewert-Verlauf mg/dL,Glukose-Scan mg/dL,Nicht numerisches schnellwirkendes Insulin,Schnellwirkendes Insulin (Einheiten),Nicht numerische Nahrungsdaten,Kohlenhydrate (Gramm),Kohlenhydrate (Portionen),Nicht numerisches Depotinsulin,Depotinsulin (Einheiten),Notizen,Glukose-Teststreifen mg/dL,Keton mmol/L,Mahlzeiteninsulin (Einheiten),Korrekturinsulin (Einheiten),Insulin-Änderung durch Anwender (Einheiten)\n"
        csv_data += f"120,2021-10-02 09:08:00\n"
        csv_data += f"130,2021-10-03 09:10:00\n"

        # Write the CSV to the temporary directory
        with open(os.path.join(self.test_dir, filename), 'w') as f:
            f.write(csv_data)

    def test_import_glucose_readings(self):
        call_command('import_glucose_readings', self.test_dir)

        readings = GlucoseReading.objects.filter(user=self.user_2)
        self.assertEqual(readings.count(), 2)

        # Clean up the temporary directory after the test
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)
