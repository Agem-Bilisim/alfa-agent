#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil

if sys.platform == 'linux':
    from alfa_agent.core.api.util.linux_util import Util
else:
    from alfa_agent.core.api.util.windows_util import Util


class Util(Util):
    @staticmethod
    def create_file(full_path):
        """
        :param full_path:
        :return:
        """
        if os.path.exists(full_path):
            return None
        elif not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))

        file = open(full_path, 'w+')
        file.close()
        return True

    @staticmethod
    def delete_folder(full_path):
        """
        :param full_path:
        :return:
        """
        shutil.rmtree(full_path)

    @staticmethod
    def delete_file(full_path):
        """
        :param full_path:
        :return:
        """
        if Util.does_exist(full_path):
            os.remove(full_path)

    @staticmethod
    def does_exist(full_path):
        """
        :param full_path:
        :return:
        """
        return os.path.exists(full_path)

    @staticmethod
    def server_url():
        return "http://192.168.1.118:8080/alfa/agent/"
