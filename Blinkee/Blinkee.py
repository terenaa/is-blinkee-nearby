# -*- coding: utf-8 -*-

from __future__ import print_function
from .BlinkeeApi import BlinkeeApi
from .BlinkeeNoScootersException import BlinkeeNoScootersException
from .Utils import Cache, Utils


class Blinkee:
    def __init__(self, origin, region_id, distance, notifier=None):
        self._origin = origin
        self._region_id = region_id
        self._distance = distance
        self._notifier = notifier
        self._cache = Cache(".cache.blinkee.json")
        self._api = BlinkeeApi()
        self._vehicles_nearby = []

    def _search(self):
        """
        Search vehicles in selected region

        :return: List of vehicles nearby
        """
        if len(self._vehicles_nearby) > 0:
            return self._vehicles_nearby

        vehicles = self._api.get_vehicles(self._region_id)

        for vehicle in vehicles:
            if "scooter" != vehicle["type"]:
                continue

            distance = int(round(Utils.haversine(float(self._origin[0]), float(self._origin[1]),
                                                 float(vehicle["position"]["lat"]), float(vehicle["position"]["lng"])),
                                 -2))

            if int(self._distance) <= distance:
                continue

            self._vehicles_nearby.append({
                "id": vehicle["id"],
                "position": vehicle["position"],
                "distance": distance
            })

        if 0 == len(self._vehicles_nearby):
            raise BlinkeeNoScootersException

        self._vehicles_nearby = sorted(self._vehicles_nearby, key=lambda v: v["distance"])

        return self._vehicles_nearby

    def show(self):
        """
        Show vehicles nearby in the terminal
        """
        try:
            vehicles_nearby = self._search()
        except BlinkeeNoScootersException:
            print("No vehicles nearby...")
            return

        print("The closest vehicle is about %i meters from your location: " % vehicles_nearby[0]["distance"], end="")
        print(Utils.map_link(self._origin[0], self._origin[1], vehicles_nearby[0]["position"]["lat"],
                             vehicles_nearby[0]["position"]["lng"]))

        if 1 == len(vehicles_nearby):
            return

        print("\n* Other vehicles nearby:")

        for vehicle in vehicles_nearby[1:4]:
            print("%i meters -> %s" % (vehicle["distance"],
                                       Utils.map_link(self._origin[0], self._origin[1], vehicle["position"]["lat"],
                                                      vehicle["position"]["lng"])))

    def notify(self):
        """
        Notify given endpoint of new vehicles
        """
        if self._notifier is None:
            return

        try:
            vehicles_nearby = self._search()
        except BlinkeeNoScootersException:
            return

        try:
            last_vehicles = self._cache.load()
        except IOError:
            last_vehicles = []

        vehicles_ids = map(lambda v: v["id"], vehicles_nearby)
        vehicles_nearby_counter = len(vehicles_nearby)
        new_vehicles = Utils.list_diff(vehicles_ids, last_vehicles)

        try:
            self._cache.save(vehicles_ids)
        except IOError:
            pass

        # No new vehicles nearby
        if 0 == len(new_vehicles):
            return

        message = "I have found new :motor_scooter: nearby! :bulb:\n\n" + \
                  "The closest vehicle is **about %i meters** from your location: %s" % (
                      vehicles_nearby[0]["distance"], Utils.map_link(self._origin[0], self._origin[1],
                                                                     vehicles_nearby[0]["position"]["lat"],
                                                                     vehicles_nearby[0]["position"]["lng"]))

        if not self._notifier.supports_embeds() or 1 == vehicles_nearby_counter:
            self._notifier.push(message)
            return

        embed = {
            "color": 7137163,
            "title": "Other :motor_scooter: nearby",
            "fields": [],
            "footer": {
                "text": "The %s %i vehicle%s in your area." % ("are" if vehicles_nearby_counter > 1 else "is",
                                                               vehicles_nearby_counter,
                                                               "" if 1 == vehicles_nearby_counter else "s")
            }
        }

        for vehicle in vehicles_nearby[1:4]:
            embed["fields"].append({
                "name": "About %i meters" % vehicle["distance"],
                "value": Utils.map_link(self._origin[0], self._origin[1], vehicle["position"]["lat"],
                                        vehicle["position"]["lng"])
            })

        self._notifier.push(message, embed)
