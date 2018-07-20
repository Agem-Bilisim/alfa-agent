#!/usr/bin/env python3
# -*- coding: utf-8 -*

import os
import psutil
import sys
from alfa_agent.core.api.util.util import Util


class System:
    class Agent(object):
        @staticmethod
        def pid_path():
            return os.path.normpath(os.path.join(System.Agent.data_path(), 'tmp', 'agent.pid'))

        @staticmethod
        def conf_path():
            return os.path.normpath(os.path.join(System.Agent.data_path(), 'conf', 'agent.ini'))

        @staticmethod
        def log_conf_path():
            return os.path.normpath(os.path.join(System.Agent.data_path(), 'conf', 'logging.yaml'))

        @staticmethod
        def data_path():
            return os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data'))

        @staticmethod
        def fifo_file():
            return os.path.normpath(os.path.join(System.Agent.data_path(), 'tmp', 'agent.fifo'))

        @staticmethod
        def is_running(pid):
            return psutil.pid_exists(pid)

        @staticmethod
        def agent_dir_path():
            return os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

        @staticmethod
        def sys_out_path():
            return os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'sys_info.json'))

    class Process(object):
        @staticmethod
        def process_by_pid(pid):
            return psutil.Process(int(pid))

    @staticmethod
    def get_python_path():
        if sys.platform == 'win32':
            path_list = os.environ['PATH'].split(os.pathsep)
            for path in path_list:
                try:
                    if 'python.exe' in os.listdir(path):
                        return os.path.join(path, 'python.exe')
                except:
                    continue
            return None
        else:
            path_list = os.environ['PATH'].split(os.pathsep)
            for path in path_list:
                try:
                    p = os.path.join(path, 'python3')
                    if Util.does_exist(p):
                        return p
                except:
                    continue
            return None
