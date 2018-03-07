#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
from core.api.system.system import System
from core.api.util.util import Util

class Fifo(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.path = System.Agent.fifo_file()
        if not Util.does_exist(self.path):
            Util.create_file(self.path)

    def push(self, content):
        file = None
        self.lock.acquire()
        try:
            file = open(self.path, 'a+')
            file.write(content)
        except Exception as e:
            print('Error:{0}'.format(str(e)))
        finally:
            file.close()
            self.lock.release()

    def pull(self, queue):
        result = None
        self.lock.acquire()
        try:
            lines = open(self.path, 'rb').readlines()
            if lines is not None and len(lines) > 0:
                result = lines[0].decode("unicode_escape")
                w_file = open(self.path, 'wb')
                w_file.writelines(lines[1:])
                w_file.close()
        except Exception as e:
            print('Error:{0}'.format(str(e)))
        finally:
            self.lock.release()
        queue.put(result)
