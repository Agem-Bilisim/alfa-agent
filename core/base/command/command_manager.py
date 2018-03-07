#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import threading
import sys
from core.api.system.system import System
from core.api.util.util import Util
from core.base.command.fifo import Fifo

class CommandManager(object):
    def __init__(self):
        self.commands = ['start', 'stop']

    def set_event(self, *args):
        try:
            if args is None or len(args) < 1:
                print('Lack of arguments')
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
            return False

    def start(self, is_running, params):
        if is_running:
            print('Agent already started')
        else:
            print('Agent is starting...')
            Util.execute('Start-Process -FilePath {0} -ArgumentList "{1} _start" -WindowStyle hidden'.format(
                System.get_python_path(), os.path.join(System.Agent.agent_dir_path(), 'agent.py')))

    def stop(self, is_running, params):
        data = dict()
        if is_running:
            data['event'] = params[1]
        else:
            print('Agent not running!')
            data = None
        return data
