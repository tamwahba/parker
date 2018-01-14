import logging
from collections import defaultdict

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import LineString

from .models import DateRange, ParkingRule, Vehicle
from .parser import Parser


def num_to_rule_type(num, inverted=False):
    action = ParkingRule.RULE_TYPES[num][0]

    if inverted and num == 0:
        action = ParkingRule.RULE_TYPES[1][0]
    elif inverted and num == 1:
        action = ParkingRule.RULE_TYPES[3][0]
    elif inverted and num == 2:
        action = ParkingRule.RULE_TYPES[5][0]

    return action


def num_to_weekday(num):
    return DateRange.WEEKDAYS[num][0]


def num_to_month(num):
    return DateRange.MONTHS[num][0]


def num_to_vehicle(num):
    return Vehicle.VEHICLE_TYPES[num][0]


def date_to_model(date):
    date_range = DateRange()

    date_range.start_weekday = num_to_weekday(date.start_day)
    date_range.start_month = num_to_month(date.start_month)
    date_range.start_day = date.start_month_day
    date_range.start_minutes = (date.start_hour.hours * 60) +\
        date.start_hour.minutes

    date_range.end_weekday = num_to_weekday(date.end_day)
    date_range.end_month = num_to_month(date.end_month)
    date_range.end_day = date.end_month_day
    date_range.end_minutes = (date.end_hour.hours * 60) +\
        date.end_hour.minutes

    return date_range


def batch_parking_rules(parking_data):
    parking_rules = []

    for parking_data_tuple in parking_data:
        (rule,
         street_segment,
         section_id,
         raw_rule,
         exclusive_vehicles
         ) = parking_data_tuple

        parking_rule = ParkingRule()

        if rule.time_limit.minutes > 0:
            parking_rule.time_limit = rule.time_limit.minutes

        parking_rule.section_id = section_id
        parking_rule.street_segment = street_segment
        parking_rule.raw_text = raw_rule
        parking_rule.rule_type = num_to_rule_type(rule.action.value,
                                                  rule.is_inverted)

        parking_rules.append(parking_rule)

    ParkingRule.objects.bulk_create(parking_rules)

    for index, parking_data_tuple in enumerate(parking_data):
        parking_rule = parking_rules[index]

        (rule,
         street_segment,
         section_id,
         raw_rule,
         exclusive_vehicles
         ) = parking_data_tuple

        date_ranges = [date_to_model(date) for date in rule.active_dates]

        DateRange.objects.bulk_create(date_ranges)

        ParkingRuleDateRange = ParkingRule.date_ranges.through
        parking_rule_date_ranges = []
        for date_range in date_ranges:
            parking_rule_date_ranges.append(
                ParkingRuleDateRange(
                    parkingrule_id=parking_rule.id,
                    daterange_id=date_range.id
                )
            )

        ParkingRuleDateRange.objects.bulk_create(parking_rule_date_ranges)

        ParkingRuleExclusiveVehicle = ParkingRule.exclusive_vehicles.through
        parking_rule_exclusive_vehicles = []
        for exclusive_vehicle in exclusive_vehicles:
            parking_rule_exclusive_vehicles.append(
                ParkingRuleExclusiveVehicle(
                    parkingrule_id=parking_rule.id,
                    vehicle_id=exclusive_vehicle.id
                )
            )

        ParkingRuleExclusiveVehicle.objects.bulk_create(
            parking_rule_exclusive_vehicles)


def import_shapefile(parser_lib_path, shapefile_path):
    logger = logging.getLogger(__name__)

    parser = Parser(parser_lib_path)

    vehicle_types = [
        Vehicle.objects.get(vehicle_type=Vehicle.VEHICLE_TYPES[0][0]),
        Vehicle.objects.get(vehicle_type=Vehicle.VEHICLE_TYPES[1][0]),
        Vehicle.objects.get(vehicle_type=Vehicle.VEHICLE_TYPES[2][0]),
    ]

    file_name = shapefile_path

    logger.info('Loading shapes from {file_name}'.format(file_name=file_name))

    ds = DataSource(file_name)
    mapping = defaultdict(lambda: defaultdict(list))
    for feature in ds[0]:
        description = feature.get('SIGNDESC1')
        section = feature.get('SG_ORDER_N')

        mapping[section][description].append(feature)

    total_to_process = len(mapping)
    processed = 0

    logger.info('Loaded {num_descriptions} unique descriptions'.format(
        num_descriptions=total_to_process))

    for section, descriptions in mapping.items():
        for description, signs in descriptions.items():
            points = [feature.geom.geos for feature in signs]

            if len(points) == 1:
                points.append(points[0])

            street_segment = LineString(points)

            with parser.parse(str.encode(description)) as rules:
                parking_rule_data = []

                for rule in rules:
                    vehicles = [vehicle_types[vehicle_type.value]
                                for vehicle_type
                                in rule.exclusive_vehicle_types]

                    parking_rule_data.append((
                        rule,
                        street_segment,
                        section,
                        description,
                        vehicles
                    ))

                batch_parking_rules(parking_rule_data)
        processed += 1
        if processed % 10000 == 0 or processed == total_to_process:
            logger.info('Processed {num_processed} out of '
                        '{num_descriptions} descriptions'.format(
                            num_processed=processed,
                            num_descriptions=total_to_process))
