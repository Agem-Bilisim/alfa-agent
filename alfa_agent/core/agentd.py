#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import alfa_agent.core.api.system.sysinfo as sysinfo
from alfa_agent.core.base.daemon.custom_daemon import Daemon
from alfa_agent.core.base.messaging.message_receiver import MessageHandler
from http.server import HTTPServer
from alfa_agent.core.api.util.util import Util


class AgentDaemon(Daemon):
    def run(self):
        # Generate messaging ID if not already exists
        if not Util.get_str_prop("AGENT", "messaging_id"):
            import uuid
            from uuid import getnode as get_mac
            # Depending of initialization of network interfaces in different order,
            # get_mac() might return different values on each run!
            # Besides it may only return invalid addresses (e.g. Bluetooth or virtual network interface)
            #
            # Therefore Alfa-server must match an agent to its database record by looking
            # not only its 'from' field but also all of its MAC addresses.
            Util.set_str_prop("AGENT", "messaging_id", str(uuid.uuid5(uuid.NAMESPACE_DNS, str(get_mac()))))

        # Refresh collected system info
        if Util.get_bool_prop("AGENT", "send_sysinfo_on_startup"):
            sysinfo.collect_and_send()

        # Start up http server
        httpd = HTTPServer(('', Util.get_int_prop("CONNECTION", "agent_port")), MessageHandler)
        httpd.serve_forever()

        while True:
            time.sleep(1)