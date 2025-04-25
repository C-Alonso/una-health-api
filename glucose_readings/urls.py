from django.urls import path
from glucose_readings.views import GlucoseReadingList, GlucoseReadingDetail

urlpatterns = [
    path('levels/', GlucoseReadingList.as_view(), name='glucose-reading-list'),
    path('levels/<int:pk>/', GlucoseReadingDetail.as_view(), name='glucose-reading-detail'),
]
