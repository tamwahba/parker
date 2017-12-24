from django.contrib.gis.geos import Point
from rest_framework import viewsets

from .models import DateRange, ParkingRule
from .serializers import DateRangeSerializer, ParkingRuleSerializer


class DateRangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DateRange.objects.all()
    serializer_class = DateRangeSerializer


class ParkingRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParkingRule.objects.all()
    serializer_class = ParkingRuleSerializer


class ParkingRuleByLocationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParkingRuleSerializer

    def get_queryset(self):
        longitude = float(self.kwargs['longitude'])
        latitude = float(self.kwargs['latitude'])
        radius = float(self.kwargs['radius'])

        point = Point(x=longitude, y=latitude)

        return ParkingRule.objects.filter(
            street_segment__dwithin=(point, radius))
