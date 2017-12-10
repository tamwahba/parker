from rest_framework import viewsets

from .models import DateRange, ParkingRule
from .serializers import DateRangeSerializer, ParkingRuleSerializer


class DateRangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DateRange.objects.all()
    serializer_class = DateRangeSerializer


class ParkingRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParkingRule.objects.all()
    serializer_class = ParkingRuleSerializer
