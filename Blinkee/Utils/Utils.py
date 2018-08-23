# -*- coding: utf-8 -*-

from math import radians, cos, sin, asin, sqrt


class Utils(object):
    @staticmethod
    def haversine(lat1, lng1, lat2, lng2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

        return int(round(2 * asin(sqrt(sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin(
            (lng2 - lng1) / 2) ** 2)) * 6371 * 1000))

    @staticmethod
    def map_link(lat1, lng1, lat2, lng2):
        return "https://www.google.com/maps/dir/?api=1&origin=%s,%s&destination=%s,%s" % (lat1, lng1, lat2, lng2)

    @staticmethod
    def list_diff(list1, list2):
        return list(set(list1) - set(list2))
