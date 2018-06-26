#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import alfa_agent.core.api.system.sysinfo as sysinfo
from alfa_agent.core.base.daemon.custom_daemon import Daemon
from alfa_agent.core.base.messaging.message_receiver import MessageHandler
from http.server import HTTPServer


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