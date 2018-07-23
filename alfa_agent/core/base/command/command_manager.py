#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import threading
import logging
import sys
from subprocess import check_output, CalledProcessError
from alfa_agent.core.api.system.system import System
from alfa_agent.core.api.util.util import Util
from alfa_agent.core.base.command.fifo import Fifo
from alfa_agent.core.base.daemon.custom_daemon import Daemon


class CommandManager(object):
    def __init__(self, logger=None):
        self.commands = ['start', 'stop', 'install']
        self.logger = logger or logging.getLogger(__name__)

    def set_event(self, *args):
        try:
            if args is None or len(args) < 1:
                self.logger.error('Missing arguments.')
                return False

            params = args[0]
            func = getattr(self, params[1].replace('-', '_'))
            data = func(params)

            if data and len(data) > 0:
                fifo = Fifo()
                thread = threading.Thread(target=fifo.push(str(json.dumps(data)) + '\n'))
                thread.start()
            return True
        except Exception as e:
            self.logger.error("Cannot start the agent process.", exc_info=True)
            return False

    def start(self, params):
        pass

    def stop(self, params):
        pid = Daemon.get_pid()
        data = dict()
        if pid:
            data['event'] = params[1]
        else:
            self.logger.warning('Agent already stopped.')
            data = None
        return data

    def install(self, params):
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin:
            self.logger.info("Installing 3rd party dependencies...")
            success = True
            if sys.platform == "win32":
                if Util.read_prop('platform_requires.win32') is not None:
                    try:
                        check_output("pip.exe install --no-input {}".format(
                            " ".join(Util.read_prop('platform_requires.win32'))).split(), universal_newlines=True)
                    except CalledProcessError as e:
                        success = False
                        self.logger.error("Error occurred during installation of PyWebView/Win32 dependencies: {}"
                                          .format(str(e)))
            elif sys.platform == "linux":
                if is_gtk_based():
                    if Util.read_prop('platform_requires.debian-gtk') is not None:
                        try:
                            check_output("apt-get install -y {}".format(" ".join(
                                Util.read_prop('platform_requires.debian-gtk'))).split(), universal_newlines=True)
                        except CalledProcessError as e:
                            success = False
                            self.logger.error("Error occurred during installation of PyWebView/GTK3.0 dependencies: {}"
                                              .format(str(e)))
                else: # QT-based
                    if Util.read_prop('platform_requires.debian-qt') is not None:
                        try:
                            check_output("apt-get install -y {}".format(" ".join(
                                Util.read_prop('platform_requires.debian-qt'))).split(), universal_newlines=True)
                        except CalledProcessError as e:
                            success = False
                            self.logger.error("Error occurred during installation of PyWebView/Qt dependencies: {}"
                                              .format(str(e)))
            else:
                self.logger.error("Failed to determine the OS! Cannot install 3rd party dependencies.")
            self.logger.log(logging.INFO if success else logging.ERROR,
                            "Successfully installed 3rd party dependencies" if success else
                            "Failed to install 3rd party dependencies. Please install the following manually: {}"
                            .format(Util.read_prop('platform_requires.win32') if sys.platform == 'win32' else
                                                                (Util.read_prop('platform_requires.debian-gtk')
                                                                 if is_gtk_based()
                                                                 else Util.read_prop('platform_requires.debian-qt'))))
        else:
            self.logger.warning("Install command invoked without elevated privileges! "
                                "Cannot install 3rd party dependencies.")


def is_gtk_based():
    try:
        output = check_output("apt-cache policy libgtk-3-0 | grep Installed".split(), universal_newlines=True)
        return "Installed" in output
    except CalledProcessError as e:
        pass
    return False
