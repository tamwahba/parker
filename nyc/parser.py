import ctypes

from contextlib import contextmanager


array_types_cache = {}


def array_of(subtype):
    if subtype in array_types_cache:
        return array_types_cache[subtype]

    class Array(ctypes.Structure):
        _fields_ = [('data', ctypes.POINTER(subtype)),
                    ('len', ctypes.c_size_t)]

        def __getitem__(self, index):
            return self.data[index]

        def __iter__(self):
            class ArrayIterator:
                def __init__(self, array):
                    self.idx = 0
                    self.array = array

                def __iter__(self):
                    return self

                def __next__(self):
                    if self.idx == self.array.len:
                        raise StopIteration

                    self.idx += 1
                    return self.array.data[self.idx - 1]

            return ArrayIterator(self)

        def __repr__(self):
            return repr([item for item in self])

    array_types_cache[subtype] = Array
    return Array


class Action(ctypes.c_uint):
    def __repr__(self):
        action = 'stopping'

        if self.value == 0:
            action = 'parking'
        elif self.value == 1:
            action = 'standing'

        return 'Action({})'.format(action)


class Time(ctypes.Structure):
    _fields_ = [('hours', ctypes.c_uint8),
                ('minutes', ctypes.c_uint8)]

    def __repr__(self):
        return 'Time(hours={}, minutes={}'.format(self.hours, self.minutes)


class Date(ctypes.Structure):
    _fields_ = [('start_day', ctypes.c_uint),
                ('end_day', ctypes.c_uint),
                ('start_hour', Time),
                ('end_hour', Time),
                ('start_month', ctypes.c_uint),
                ('start_month_day', ctypes.c_uint8),
                ('end_month', ctypes.c_uint),
                ('end_month_day', ctypes.c_uint8)]

    def __repr__(self):
        return 'Date(start_day={}, start_hour={}, start_month={}, '\
            'start_month_day={}, end_day={}, end_hour={}, end_month={}, '\
            'end_month_day={})'.format(
                self.start_day, self.start_hour, self.start_month,
                self.start_month_day, self.end_day, self.end_hour,
                self.end_month, self.end_month_day)


class TimeLimit(ctypes.Structure):
    _fields_ = [('minutes', ctypes.c_uint16)]

    def __repr__(self):
        return 'TimeLimit({})'.format(self.minutes)


class Vehicle(ctypes.c_uint):
    def __repr__(self):
        vehicle = 'trucks'

        if self.value == 0:
            vehicle = 'private'
        elif self.value == 1:
            vehicle = 'commercial'

        return 'Vehicle({})'.format(vehicle)


class ParsedRule(ctypes.Structure):
    _fields_ = [('active_dates', array_of(Date)),
                ('action', Action),
                ('is_inverted', ctypes.c_bool),
                ('time_limit', TimeLimit),
                ('exclusive_vehicle_types', array_of(Vehicle))]

    def __repr__(self):
        return 'ParkingRule(active_dates={}, action={}, is_inverted={}, '\
            'time_limit={}, exclusive_vehicle_types={})'.format(
                self.active_dates, self.action, self.is_inverted,
                self.time_limit, self.exclusive_vehicle_types)


class Parser:
    def __init__(self, library_path):
        libparser = ctypes.cdll.LoadLibrary(library_path)

        self.ext_parse = libparser.rules_from_str
        self.ext_parse.argtypes = [ctypes.c_char_p]
        self.ext_parse.restype = array_of(ParsedRule)

        self.ext_free = libparser.free_rules
        self.ext_free.argtypes = [array_of(ParsedRule)]
        self.ext_free.restype = None

    @contextmanager
    def parse(self, string):
        rules = self.ext_parse(string)
        try:
            yield rules
        finally:
            self.ext_free(rules)
