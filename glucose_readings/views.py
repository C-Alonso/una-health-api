from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from glucose_readings.models import GlucoseReading
from glucose_readings.serializers import GlucoseReadingSerializer
import django_filters


class GlucoseReadingPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class GlucoseReadingFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(field_name="user__id")
    start = django_filters.DateTimeFilter(field_name="reading_datetime", lookup_expr='gte')
    stop = django_filters.DateTimeFilter(field_name="reading_datetime", lookup_expr='lte')

    class Meta:
        model = GlucoseReading
        fields = ['user_id', 'start', 'stop']


# View for listing glucose readings with pagination and sorting
class GlucoseReadingList(APIView):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GlucoseReadingFilter
    pagination_class = GlucoseReadingPagination
    ordering_fields = ['glucose_level', 'reading_datetime']
    ordering = ['reading_datetime']


    def get(self, request, *args, **kwargs):

        user_id = self.request.query_params.get('user_id')

        if not user_id:
            raise ValidationError({"user_id": "This query parameter is required."})

        queryset = GlucoseReading.objects.all()
        filter_backend = self.filter_backends[0]()
        queryset = filter_backend.filter_queryset(self.request, queryset, self)

        # Apply ordering
        ordering_fields = self.ordering_fields
        ordering = self.request.query_params.get('ordering', None)
        if ordering in ordering_fields:
            queryset = queryset.order_by(ordering)

        # Apply pagination
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = GlucoseReadingSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# View for retrieving a specific glucose reading by id
class GlucoseReadingDetail(generics.RetrieveAPIView):
    queryset = GlucoseReading.objects.all()
    serializer_class = GlucoseReadingSerializer
