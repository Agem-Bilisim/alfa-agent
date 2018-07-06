#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# FIXME: path must be read from System.py but first fix cyclic import!
DATA_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data'))
INI_PATH = os.path.normpath(os.path.join(DATA_PATH, 'conf', 'agent.ini'))


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

        # TODO we should respect file owner!
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
        config = ConfigParser()
        config.read(INI_PATH, encoding='utf8')
        return config.get(section, prop)

    @staticmethod
    def get_bool_prop(section, prop):
        config = ConfigParser()
        config.read(INI_PATH, encoding='utf8')
        return config.getboolean(section, prop)

    @staticmethod
    def get_int_prop(section, prop):
        config = ConfigParser()
        config.read(INI_PATH, encoding='utf8')
        return config.getint(section, prop)

    @staticmethod
    def set_str_prop(section, prop, val):
        config = ConfigParser()
        config.read(INI_PATH, encoding='utf8')
        config[section][prop] = val
        with open(INI_PATH, 'w') as f:
            config.write(f)
