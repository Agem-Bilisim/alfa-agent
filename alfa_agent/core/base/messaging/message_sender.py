#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import threading
from core.api.util.util import Util


class MessageSender:
    def __init__(self, url):
        self.url = url
        self.headers = {'content-type': 'application/json'}

    def send(self, payload):
        t = threading.Thread(target=worker, kwargs=dict(url=self.url, headers=self.headers, payload=payload))
        t.start()


def worker(url=None, headers=None, payload=None):
    try:
        _payload = json.loads(payload) if type(payload) is str else payload
        _payload['from'] = Util.get_str_prop("AGENT", "messaging_id")
        assert _payload['from']
        print("Sending message with payload: {}".format(json.dumps(_payload)))
        resp = requests.post(url, data=json.dumps(_payload), headers=headers)
        print("Sent message to url:" + url if resp is not None and resp.status_code == 200 else
              "Failed to send message to url:" + url)
    except ConnectionError as e:
        print(e)
