#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging.config
from elevate import elevate
import yaml

# This is an ugly workaround to ensure all module imports work properly when running the agent locally.
# See https://stackoverflow.com/questions/1893598/pythonpath-vs-sys-path and
# https://askubuntu.com/questions/470982/how-to-add-a-python-module-to-syspath/471168 for more info.
# -----------------------------------------------------------------------
MODULE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if MODULE_PATH not in sys.path:
    sys.path.insert(1, MODULE_PATH)
# -----------------------------------------------------------------------

from alfa_agent.core.agentd import AgentDaemon
from alfa_agent.core.api.system.system import System
from alfa_agent.core.base.command.command_manager import CommandManager
from alfa_agent.core.api.util.util import Util

try:
    is_admin = os.getuid() == 0
except AttributeError:
    import ctypes
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

should_elevate = Util.read_prop("agent.send_sysinfo_on_startup")
if not is_admin and should_elevate:
    elevate(show_console=False)


def agent(args=None):
    """
    Entry point for the ALFA agent
    :param args:
    :return:
    """
    # Configure logging
    setup_logging(default_level=Util.read_prop("agent.logging_level"))
    logger = logging.getLogger(__name__)
    if args and len(args) > 0 and args[1] == '_start':
        agent_daemon = AgentDaemon(System.Agent.pid_path())
        agent_daemon.start()
    else:
        logger.info('Passing script parameters to the agent...')
        logger.info('Event: {}, parameters: {}'.format(args[1], args[1:]))
        cmd = CommandManager()
        result = cmd.set_event(args)
        if not result:
            logger.info('Unknown event or parameter. Usage : {} {}'.format(args[0], '|'.join(cmd.commands)))
            sys.exit(1)


def setup_logging(
    default_path=System.Agent.log_conf_path(),
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':
    agent(sys.argv)
