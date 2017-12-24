from django.contrib.gis import admin

from .models import DateRange, ParkingRule


class ParkingRuleAdmin(admin.OSMGeoAdmin):
    raw_id_fields = ('date_ranges', )


admin.site.register(DateRange)
admin.site.register(ParkingRule, ParkingRuleAdmin)
