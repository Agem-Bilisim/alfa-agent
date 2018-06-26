#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import stat
import subprocess


class Util:
    def __init__(self):
        super().__init__()

    # TODO
    @staticmethod
    def close_session(username):
        print('session close for user {0}'.format(username))
        # Util.execute('pkill -9 -u {0}'.format(username))

    # TODO TEST
    @staticmethod
    def make_executable(full_path):
        try:
            st = os.stat(full_path)
            os.chmod(full_path, st.st_mode | stat.S_IXUSR)
        except:
            raise

    # TODO TEST
    @staticmethod
    def change_owner(full_path, user_name=None, group_name=None):
        try:
            shutil.chown(full_path, user_name, group_name)
        except:
            raise

    # TODO
    @staticmethod
    def execute(command, result=True, as_user=None):
        try:
            # TODO as user
            # if as_user is not None:
            #     command = 'su - {0} -c "{1}"'.format(as_user, command)
            process = subprocess.Popen(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Unrestricted', '-Command',
                                        command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result:
                result_code = process.wait()
                p_out = process.stdout.read().decode('utf-8')
                p_err = process.stderr.read().decode('utf-8')

                return result_code, p_out, p_err
            else:
                return None, None, None
        except Exception as e:
            return 1, 'Could not execute command: {0}. Error Message: {1}'.format(command, str(e)), ''

    # TODO TEST
    @staticmethod
    def execute_script(script_path, parameters=None, result=True):
        try:
            process = subprocess.Popen(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command',
                                        script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result:
                result_code = process.wait()
                p_out = process.stdout.read().decode('utf-8')
                p_err = process.stderr.read().decode('utf-8')

                return result_code, p_out, p_err
            else:
                return None, None, None
        except Exception as e:
            return 1, 'Could not execute script: {0}. Error Message: {1}'.format(script_path, str(e)), ''

    # TODO TEST
    # linux
    # @staticmethod
    # def file_owner(full_path):
    #     try:
    #         st = os.stat(full_path)
    #         uid = st.st_uid
    #         return pwd.getpwuid(uid)[0]
    #     except:
    #         raise

    # @staticmethod
    # def file_group(full_path):
    #     try:
    #         st = os.stat(full_path)
    #         gid = st.st_uid
    #         return grp.getgrgid(gid)[0]
    #     except:
    #         raise

    # TODO install / uninstall / isinstalled


    @staticmethod
    def set_permission(path, permission_code):
        """look for modes: https://docs.python.org/3/library/stat.html#stat.S_ISUID"""
        os.chmod(path, permission_code)

    # TODO TEST
    @staticmethod
    def get_environment_variables(path):
        try:
            return os.environ[path]
        except:
            return None

    # TODO TEST
    @staticmethod
    def add_environment_variable(path, value):
        try:
            os.environ[path] += ';' + value
        except:
            raise
