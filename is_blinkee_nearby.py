# -*- coding: utf-8 -*-

from Notifier import Discord
from Blinkee import Blinkee, BlinkeeApi

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument("-s", "--search", action="store_true", help="search scooters nearby")
    exclusive_group.add_argument("-a", "--regions", action="store_true", help="show available regions")

    searching_group = parser.add_argument_group("Search scooters nearby")
    searching_group.add_argument("-o", "--origin", help="starting point coordinates xx.xxx,yy.yyy")
    searching_group.add_argument("-r", "--region", help="chosen region ID")
    searching_group.add_argument("-d", "--distance", help="distance in meters")

    parser.add_argument("-w", "--webhook", help="notifier webhook url", required=False)

    args = parser.parse_args()

    if args.regions:
        regions = BlinkeeApi().get_regions()

        if not regions:
            print("No available regions.")

        row_format = u"{:<5}" * 2
        print("Available regions:\n")
        print(row_format.format("ID", "Region"))
        print(row_format.format("--", "------"))

        for region in regions:
            print(row_format.format(region["id"], region["name"]))
    elif args.search:
        if args.origin is None or args.region is None or args.distance is None:
            parser.error("Search option requires origin, region and distance.")

        discord = Discord(args.webhook) if args.webhook is not None else None
        blinkee = Blinkee(origin=tuple(args.origin.split(",")), region_id=int(args.region), distance=int(args.distance),
                          notifier=discord)

        blinkee.show()
        blinkee.notify()
