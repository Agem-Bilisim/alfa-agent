#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import stat
import pwd
import subprocess


class Util:
    def __init__(self):
        super().__init__()

    # linux
    @staticmethod
    def close_session(username):
        Util.execute('pkill -9 -u {0}'.format(username))

    @staticmethod
    def make_executable(full_path):
        try:
            st = os.stat(full_path)
            os.chmod(full_path, st.st_mode | stat.S_IEXEC)
        except:
            raise

    @staticmethod
    def change_owner(full_path, user_name=None, group_name=None):
        try:
            shutil.chown(full_path, user_name, group_name)
        except:
            raise

    @staticmethod
    def execute(command, stdin=None, env=None, cwd=None, shell=True, result=True, as_user=None):

        try:
            if as_user is not None:
                command = 'su - {0} -c "{1}"'.format(as_user, command)
                pw_record = pwd.getpwnam(as_user)
                user_uid = pw_record.pw_uid
                user_gid = pw_record.pw_gid
            process = subprocess.Popen(command, stdin=stdin, env=env, cwd=cwd, stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE, shell=shell,
                                       preexec_fn=_set_ids(user_uid, user_gid) if as_user is not None else None)

            if result is True:
                result_code = process.wait()
                p_out = process.stdout.read().decode("unicode_escape")
                p_err = process.stderr.read().decode("unicode_escape")

                return result_code, p_out, p_err
            else:
                return None, None, None
        except Exception as e:
            return 1, 'Could not execute command: {0}. Error Message: {1}'.format(command, str(e)), ''

    @staticmethod
    def execute_script(script_path, parameters=None):
        command = []
        if os.path.exists(script_path):
            command.append(script_path)
        else:
            raise Exception('Script is required')

        if parameters is not None:
            for p in parameters:
                command.append(p)

        return subprocess.check_call(command)

    @staticmethod
    def install_with_gdebi(full_path):
        try:
            process = subprocess.Popen('gdebi -n ' + full_path, shell=True)
            process.wait()
        except:
            raise

    @staticmethod
    def install_with_apt_get(package_name, package_version=None):

        if package_version is not None:
            command = 'apt-get install --yes --force-yes {0}={1}'.format(package_name, package_version)
        else:
            command = 'apt-get install --yes --force-yes {0}'.format(package_name)

        return Util.execute(command)

    @staticmethod
    def uninstall_package(package_name, package_version=None):

        if package_version is not None:
            command = 'apt-get purge --yes --force-yes {0}={1}'.format(package_name, package_version)
        else:
            command = 'apt-get purge --yes --force-yes {0}'.format(package_name)

        return Util.execute(command)

    @staticmethod
    def is_installed(package_name):

        result_code, p_out, p_err = Util.execute('dpkg -s {0}'.format(package_name))
        try:
            lines = str(p_out).split('\n')
            for line in lines:
                if len(line) > 1:
                    if line.split(None, 1)[0].lower() == 'status:':
                        if 'installed' in line.split(None, 1)[1].lower():
                            return True
            return False
        except Exception as e:
            return False

    @staticmethod
    def set_permission(path, permission_code):
        Util.execute('chmod -R {0} {1}'.format(permission_code, path))

    @staticmethod
    def send_notify(title, body, display=None, user=None, icon=None, timeout=5000):

        inner_command = 'notify-send "{0}" "{1}" -t {2}'.format(title, body, timeout)
        if icon:
            inner_command += ' -i {0}'.format(icon)

        if user != 'root':
            Util.execute('export DISPLAY={0}; su - {1} -c \'{2}\''.format(display, user, inner_command))

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

    # TODO add docstring to this method
    @staticmethod
    def check_and_install_apt_package(package_name):
        if package_name is not None and package_name:
            if Util.is_installed(package_name):
                return '0', 'Package \'{0}\' is already installed.'.format(package_name), None
            else:
                return Util.install_with_apt_get(package_name)
        else:
            return '1', \
                   None, \
                   'Package name parameter cannot not be an empty str or None.' \
                   'Given package name: {0}'.format(package_name)

def _set_ids(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result
