#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys

from alfa_agent.core.agentd import AgentDaemon
from alfa_agent.core.api.system.system import System
from alfa_agent.core.base.command.command_manager import CommandManager

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
    main(sys.argv)
