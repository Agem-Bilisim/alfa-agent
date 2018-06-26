#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of Lider Ahenk.
#
# Lider Ahenk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Lider Ahenk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Lider Ahenk.  If not, see <http://www.gnu.org/licenses/>.


import os
import psutil
from alfa_agent.core.api.system.system import System
from alfa_agent.core.api.util.util import Util


class Daemon:
    def __init__(self, pid_path):
        self.pid_path = pid_path

    def start(self):
        if self.get_pid():
            print('Agent is already running with pid: {}'.format(self.get_pid()))
            return
        else:
            try:
                self.clear_tmp()

                Util.create_file(self.pid_path)
                pid_file = open(self.pid_path, 'w')
                pid_file.write(str(os.getpid()))
                pid_file.close()

                print('Agent started with pid: {}'.format(self.get_pid()))
            except Exception as e:
                print('A problem occurred while trying to start Agent. Error Message {0}'.format(str(e)))
                return

            self.run()

    def clear_tmp(self):
        Util.delete_folder(os.path.dirname(self.pid_path))

    def stop(self):
        try:
            if self.get_pid():
                pid = self.get_pid()
                self.del_pid()
                p = psutil.Process(int(pid))
                p.terminate()
                Util.delete_file(System.Agent.fifo_file())
            else:
                print('Could not find any process.')
        except Exception as e:
            print('A problem occurred while trying to stop Ahenk. Error Message {0}'.format(str(e)))

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
