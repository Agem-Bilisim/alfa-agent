#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import core.api.system.sysinfo as sysinfo
from core.base.daemon.custom_daemon import Daemon
from core.base.messaging.message_receiver import MessageHandler
from http.server import HTTPServer
from core.api.util.util import Util


class AgentDaemon(Daemon):
    def run(self):

        # Refresh collected system info
        if Util.get_bool_prop("AGENT", "send_sysinfo_on_startup"):
            sysinfo.collect_and_send()

        # Start up http server
        httpd = HTTPServer(('', Util.get_int_prop("CONNECTION", "agent_port")), MessageHandler)
        httpd.serve_forever()

        #httpd.server_close()
        print("serve_forever passed")
        while True:
            time.sleep(1)