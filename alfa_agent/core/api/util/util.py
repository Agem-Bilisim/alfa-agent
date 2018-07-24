#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import yaml
import sys

# FIXME: path must be read from System.py but first fix cyclic import!
DATA_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data'))
CONF_PATH = os.path.normpath(os.path.join(DATA_PATH, 'conf', 'config.yaml'))


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

        # Change owner of the newly created file to match with the owner of the parent directory
        # This prevents any permission conflict when running the agent.
        # BUT this is only for Debian-based system, Windows DOES NOT have a simple method to change owner :(
        if sys.platform == 'linux':
            parent = os.path.normpath(os.path.join(full_path, '..'))
            if os.path.exists(parent):
                os.chown(full_path, os.stat(parent).st_uid, os.stat(parent).st_gid)

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
    def read_prop(key):
        with open(CONF_PATH, 'rt') as f:
            config = yaml.safe_load(f.read())
        _config = config
        keys = str(key).split('.')
        for k in keys:
            _config = _config.get(k) if k in _config else None
            if _config is None:
                break
        return _config

    @staticmethod
    def write_prop(key, val):
        with open(CONF_PATH, 'rt') as i:
            config = yaml.safe_load(i.read())
        _config = config
        keys = key.split('.')
        latest = keys.pop()
        for k in keys:
            _config = _config.setdefault(k, {})
        _config.setdefault(latest, val)
        with open(CONF_PATH, 'wt') as o:
            o.write(yaml.dump(config, default_flow_style=False))
