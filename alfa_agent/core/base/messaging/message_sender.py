#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import threading
import logging
from alfa_agent.core.api.util.util import Util


class MessageSender:
    def __init__(self, url):
        self.url = url
        self.headers = {'content-type': 'application/json'}

    def send(self, payload):
        t = threading.Thread(target=worker, kwargs=dict(url=self.url, headers=self.headers, payload=payload))
        t.start()


def worker(url=None, headers=None, payload=None):
    logger = logging.getLogger(__name__)
    try:
        _payload = json.loads(payload) if type(payload) is str else payload
        _payload['from'] = Util.read_prop("agent.messaging_id")
        assert _payload['from']
        logger.debug("Sending message with payload: {}".format(json.dumps(_payload)))
        resp = requests.post(url, data=json.dumps(_payload), headers=headers)
        logger.info("Sent message to url:" + url if resp is not None and resp.status_code == 200
                    else "Failed to send message to url:" + url)
    except ConnectionError as e:
        logger.error("Cannot connect to server.", exc_info=True)
