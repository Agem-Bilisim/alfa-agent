#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

config = ConfigParser()
# FIX cyclic import!
DATA_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data'))
config.read(os.path.normpath(os.path.join(DATA_PATH, 'conf', 'agent.ini')), encoding='utf8')


class Util:
    @staticmethod
    def create_file(full_path, mode=0o777):
        """
        :param full_path:
        :param mode:
        :return:
        """
        if os.path.exists(full_path):
            return None
        elif not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path), mode=mode, exist_ok=True)

        file = open(full_path, 'w+')
        file.close()
        return True

    @staticmethod
    def delete_folder(full_path, ignore_errors=False):
        """
        :param full_path:
        :param ignore_errors:
        :return:
        """
        shutil.rmtree(full_path, ignore_errors)

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
    def get_str_prop(section, prop):
        return config.get(section, prop)

    @staticmethod
    def get_bool_prop(section, prop):
        return config.getboolean(section, prop)

    @staticmethod
    def get_int_prop(section, prop):
        return config.getint(section, prop)
