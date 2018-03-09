#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys

from core.agentd import AgentDaemon
from core.api.system.system import System
from core.base.command.command_manager import CommandManager

def main(args=None):
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


class Ahenk:
    @staticmethod
    def run(args):
        main(args)


if __name__ == '__main__':
    # Agent needs Python version 3.5!
    #assert sys.version_info >= (3,5)
    main(sys.argv)
