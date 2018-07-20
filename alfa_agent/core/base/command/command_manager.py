#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import threading
import logging
from alfa_agent.core.api.system.system import System
from alfa_agent.core.api.util.util import Util
from alfa_agent.core.base.command.fifo import Fifo


class CommandManager(object):
    def __init__(self, logger=None):
        self.commands = ['start', 'stop']
        self.logger = logger or logging.getLogger(__name__)

    def set_event(self, *args):
        try:
            if args is None or len(args) < 1:
                self.logger.error('Missing arguments.')
                return False

            params = args[0]
            is_running = System.Agent.is_running()
            func = getattr(self, params[1].replace('-', '_'))
            data = func(is_running, params)

            if data and len(data) > 0:
                fifo = Fifo()
                thread = threading.Thread(target=fifo.push(str(json.dumps(data)) + '\n'))
                thread.start()
            return True
        except Exception as e:
            self.logger.error("Cannot start the agent process.", exc_info=True)
            return False

    def start(self, is_running, params):
        if is_running:
            self.logger.warning('Agent already running')
        else:
            self.logger.info('Starting the agent...')
            # TODO
            Util.execute('Start-Process -FilePath {0} -ArgumentList "{1} _start" -WindowStyle hidden'.format(
                System.get_python_path(), os.path.join(System.Agent.agent_dir_path(), 'agent.py')))

    def stop(self, is_running, params):
        data = dict()
        if is_running:
            data['event'] = params[1]
        else:
            self.logger.info('Agent already stopped.')
            data = None
        return data
