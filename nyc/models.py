from django.contrib.gis.db import models


class DateRange(models.Model):
    WEEKDAYS = (
        ('sun', 'Sunday'),
        ('mon', 'Monday'),
        ('tues', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thurs', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
    )

    MONTHS = (
        ('jan', 'January'),
        ('feb', 'February'),
        ('mar', 'March'),
        ('apr', 'April'),
        ('may', 'May'),
        ('june', 'June'),
        ('july', 'July'),
        ('aug', 'August'),
        ('sept', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December'),
    )

    start_weekday = models.CharField(choices=WEEKDAYS, max_length=5)
    start_month = models.CharField(choices=MONTHS, max_length=4)
    start_day = models.IntegerField()
    start_minutes = models.IntegerField()

    end_weekday = models.CharField(choices=WEEKDAYS, max_length=5)
    end_month = models.CharField(choices=MONTHS, max_length=4)
    end_day = models.IntegerField()
    end_minutes = models.IntegerField()


class Vehicle(models.Model):
    VEHICLE_TYPES = (
        ('pr', 'Private'),
        ('cm', 'Commercial'),
        ('tr', 'Truck'),
    )

    vehicle_type = models.CharField(choices=VEHICLE_TYPES,
                                    max_length=2,
                                    unique=True)

    def __str__(self):
        name = 'UNKNOWN'

        for (key, value) in self.VEHICLE_TYPES:
            if key == self.vehicle_type:
                name = value
                break

        return name


class ParkingRule(models.Model):
    RULE_TYPES = (
        ('ypark', 'Parking Allowed'),
        ('npark', 'Parking Prohibited'),
        ('ystand', 'Standing Allowed'),
        ('nstand', 'Standing Prohibited'),
        ('ystop', 'Stopping Allowed'),
        ('nstop', 'Stopping Prohibited'),
    )

    date_ranges = models.ManyToManyField(DateRange)
    exclusive_vehicles = models.ManyToManyField(Vehicle)
    raw_text = models.CharField(max_length=200)
    rule_type = models.CharField(choices=RULE_TYPES, max_length=6)
    section_id = models.CharField(max_length=12)
    street_segment = models.LineStringField()
    time_limit = models.IntegerField(default=None, blank=True, null=True)
