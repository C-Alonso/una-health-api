from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from glucose_readings.models import GlucoseReading
from datetime import datetime


class GlucoseReadingApiTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(username="user2", email="user2@example.com", password="password")

        self.glucose1 = GlucoseReading.objects.create(user=self.user1, glucose_level=100,
                                                      reading_datetime=datetime(2021, 10, 10, 9, 0))
        self.glucose2 = GlucoseReading.objects.create(user=self.user1, glucose_level=150,
                                                      reading_datetime=datetime(2021, 10, 11, 9, 0))
        self.glucose3 = GlucoseReading.objects.create(user=self.user1, glucose_level=130,
                                                      reading_datetime=datetime(2021, 10, 12, 9,
                                                                                0))

        self.glucose4 = GlucoseReading.objects.create(user=self.user2, glucose_level=120,
                                                      reading_datetime=datetime(2021, 10, 10, 9, 0))

    def test_glucose_reading_list_pagination(self):
        url = reverse('glucose-reading-list')
        response = self.client.get(url, {'user_id': self.user1.id, 'page_size': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_glucose_reading_list_multiple_pages(self):
        url = reverse('glucose-reading-list')
        response = self.client.get(url, {'user_id': self.user1.id, 'page_size': 1, 'page': 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['glucose_level'],
                         150)

    def test_glucose_reading_sorting_and_pagination(self):
        url = reverse('glucose-reading-list')
        response = self.client.get(url, {'user_id': self.user1.id, 'ordering': 'glucose_level', 'page_size': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['glucose_level'], 100)

    def test_glucose_reading_start_filter(self):
        url = reverse('glucose-reading-list')
        start_datetime = '2021-10-11T00:00:00Z'
        response = self.client.get(url, {'user_id': self.user1.id, 'start': start_datetime})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['glucose_level'], 150)
        self.assertEqual(response.data['results'][1]['glucose_level'], 130)

    def test_glucose_reading_stop_filter(self):
        url = reverse('glucose-reading-list')
        stop_datetime = '2021-10-11T00:00:00Z'
        response = self.client.get(url, {'user_id': self.user1.id, 'stop': stop_datetime})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['glucose_level'], 100)

    def test_glucose_reading_start_and_stop_filter(self):
        url = reverse('glucose-reading-list')
        start_datetime = '2021-10-10T09:00:00Z'
        stop_datetime = '2021-10-11T00:00:00Z'
        response = self.client.get(url, {'user_id': self.user1.id, 'start': start_datetime, 'stop': stop_datetime})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only 1 reading should be returned
        self.assertEqual(response.data['results'][0]['glucose_level'], 100)  # Only glucose1 should match
