# -*- coding: utf-8 -*-

import requests
from . import Notifier


class Discord(Notifier.Notifier):
    def push(self, message=None, embeds=None):
        requests.post(self._webhook_url, json={"content": message, "embeds": [embeds] if embeds is not None else []})

    @staticmethod
    def supports_embeds():
        return True
