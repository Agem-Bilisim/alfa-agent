#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import threading

class MessageSender:
    def __init__(self, url):
        self.url = url
        self.headers = {'content-type': 'application/json'}

    def send(self, payload):
        t = threading.Thread(target=worker, kwargs=dict(url=self.url, headers=self.headers, payload=payload))
        t.start()


def worker(url=None, headers=None, payload=None):
    try:
        requests.post(url, data=payload if type(payload) is str else json.dumps(payload), headers=headers)
    except ConnectionError as e:
        print(e)
