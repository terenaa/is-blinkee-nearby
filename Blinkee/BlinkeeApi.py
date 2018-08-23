# -*- coding: utf-8 -*-

import requests


class BlinkeeApi:
    def __init__(self, endpoint="https://blinkee.city/api"):
        self._endpoint = endpoint

    def get_regions(self):
        """
        Get list of available regions

        :return: List of regions
        """
        r = requests.get("%s/regions" % self._endpoint)

        if 200 != r.status_code:
            r.raise_for_status()

        json = r.json()

        return json["data"]["items"]

    def get_vehicles(self, region_id):
        """
        Get list of vehicles in given region

        :param int region_id: ID of chosen region. List of regions is possible to obtain by get_regions method
        :return: List of vehicles
        """
        r = requests.get("%s/regions/%i/vehicles" % (self._endpoint, region_id))

        if 200 != r.status_code:
            r.raise_for_status()

        json = r.json()

        return json["data"]["items"]
