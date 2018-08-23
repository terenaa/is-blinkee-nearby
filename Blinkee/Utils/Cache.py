# -*- coding: utf-8 -*-

import json


class Cache:
    def __init__(self, cache_file=".cache.json"):
        self._cache_file = cache_file

    def save(self, data):
        with open(self._cache_file, "w") as c_file:
            json.dump(data, c_file)

    def load(self):
        with open(self._cache_file, "r") as c_file:
            data = json.load(c_file)

        return data
