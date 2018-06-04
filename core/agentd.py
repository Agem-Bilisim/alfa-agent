#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import core.api.system.sysinfo as sysinfo
from core.base.daemon.custom_daemon import Daemon
from core.base.messaging.message_receiver import MessageHandler
from http.server import HTTPServer, BaseHTTPRequestHandler


class AgentDaemon(Daemon):
    def run(self):
        """ docstring"""

        # Refresh collected system info
        sysinfo.collect_and_send()

        # Start up http server
        httpd = HTTPServer(('', 8484), MessageHandler)
        httpd.serve_forever()

        #httpd.server_close()
        print("serve_forever passed")
        while True:
            time.sleep(1)