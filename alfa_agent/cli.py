#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import os

from core.agentd import AgentDaemon
from core.api.system.system import System
from core.base.command.command_manager import CommandManager
from core.api.util.util import Util
from elevate import elevate

try:
    is_admin = os.getuid() == 0
except AttributeError:
    import ctypes
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

should_elevate = Util.get_bool_prop("AGENT", "send_sysinfo_on_startup")

if not is_admin and should_elevate:
    elevate(show_console=False)


def agent(args=None):
    if args and len(args) > 0 and args[1] == '_start':
        agent_daemon = AgentDaemon(System.Agent.pid_path())
        agent_daemon.start()
    else:
        print('Passing script parameters to the agent...')
        print('Event: {}, parameters: {}'.format(args[1], args[1:]))
        cmd = CommandManager()
        result = cmd.set_event(args)
        if not result:
            print('Unknown event or parameter. Usage : {} {}'.format(args[0], '|'.join(cmd.commands)))
            sys.exit(1)


if __name__ == '__main__':
    agent(sys.argv)
