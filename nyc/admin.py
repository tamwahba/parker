from django.contrib import admin

from .models import DateRange, ParkingRule


class ParkingRuleAdmin(admin.ModelAdmin):
    raw_id_fields = ('date_ranges', )


admin.site.register(DateRange)
admin.site.register(ParkingRule, ParkingRuleAdmin)
