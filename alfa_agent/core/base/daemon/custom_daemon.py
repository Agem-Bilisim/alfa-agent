#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import psutil
import logging
from alfa_agent.core.api.system.system import System
from alfa_agent.core.api.util.util import Util


class Daemon:
    def __init__(self, pid_path, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.pid_path = pid_path

    def start(self):
        if self.get_pid():
            self.logger.warning('Agent is already running with pid: {}'.format(self.get_pid()))
            return
        else:
            try:
                Util.create_file(self.pid_path, mode=0o775)
                with open(self.pid_path, 'w') as pid_file:
                    pid_file.write(str(os.getpid()))

                self.logger.info('Agent started with pid: {}'.format(self.get_pid()))
            except Exception as e:
                self.logger.error('Cannot start the agent.', exc_info=True)
                return

            self.run()

    def stop(self):
        try:
            if self.get_pid():
                pid = self.get_pid()
                self.del_pid()
                p = psutil.Process(int(pid))
                p.terminate()
                Util.delete_file(System.Agent.fifo_file())
            else:
                self.logger.warning('Could not find any process... It may have been already stopped.')
        except Exception as e:
            self.logger.error('Cannot stop the agent.', exc_info=True)

    def del_pid(self):
        Util.delete_file(self.pid_path)

    def get_pid(self):
        try:
            if os.path.exists(self.pid_path):
                pid_file = open(self.pid_path, 'r')
                pid = pid_file.read().strip()
            else:
                raise Exception
            if pid:
                if System.Process.process_by_pid(pid) is not None:  # Is process really active?
                    return pid
                else:
                    self.del_pid()
                    return None
            else:
                return None
        except:
            return None

    def run(self):
        pass
