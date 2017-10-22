from django.contrib import admin

from .models import DateRange, ParkingRule

admin.site.register(DateRange)
admin.site.register(ParkingRule)
