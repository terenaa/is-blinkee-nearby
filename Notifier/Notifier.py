# -*- coding: utf-8 -*-


class Notifier(object):
    def __init__(self, webhook_url):
        self._webhook_url = webhook_url

    def push(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def supports_embeds():
        raise NotImplementedError
