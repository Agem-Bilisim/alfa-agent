#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time
from core.base.daemon.custom_daemon import Daemon

class AgentDaemon(Daemon):
    def run(self):
        """ docstring"""

        while True:
            time.sleep(1)
