from rest_framework import serializers

from .models import DateRange, ParkingRule, Vehicle


class DateRangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DateRange
        fields = (
            'start_weekday',
            'start_month',
            'start_day',
            'start_minutes',
            'end_weekday',
            'end_month',
            'end_day',
            'end_minutes',
        )


class ParkingRuleSerializer(serializers.HyperlinkedModelSerializer):
    date_ranges = DateRangeSerializer(many=True)
    exclusive_vehicles = serializers.SlugRelatedField(
        many=True,
        queryset=Vehicle.objects.all(),
        slug_field='vehicle_type'
    )

    class Meta:
        model = ParkingRule
        fields = (
            'date_ranges',
            'exclusive_vehicles',
            'raw_text',
            'rule_type',
            'section_id',
            'street_segment',
            'time_limit',
        )
