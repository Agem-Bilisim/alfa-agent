#!/usr/bin/env python

"""

Print (and write to JSON file) system information in a cross-platform manner.

Output contains information about platform, BIOS, CPU, memory, disk, GPU, network, peripheral devices, installed
packages, motherboard and users.

This script heavily relies on psutil and some other bash/powershell commands. See requirements.txt for dependency list.

Debian/Ubunt/Mint:

> sudo python3 collect-sysinfo.py

Windows7/8/10 (with admin privileges):

> python3.exe collect-sysinfo.py

"""

import platform
import cpuinfo
import psutil
import sys
import json
import socket
import subprocess
import pprint
import re
from core.api.system.system import System

def collect():
    info = dict()
    pp = pprint.PrettyPrinter(indent=4)

    # Platform
    uname_result = platform.uname()
    pl = dict()
    pl['system'] = uname_result.system
    pl['node'] = uname_result.node
    pl['release'] = uname_result.release
    pl['version'] = uname_result.version
    pl['machine'] = uname_result.machine
    info['platform'] = pl

    # Running processes/services
    proc = list()
    for p in psutil.process_iter():
        # DO NOT retrieve all attrs since it is too slow!
        proc.append(p.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'cpu_times', 'memory_info']))
    info['processes'] = proc

    # BIOS
    bios = dict()
    if sys.platform == 'win32':
        print('TODO')
    else:
        bios['vendor'] = subprocess.check_output("dmidecode --string bios-vendor", universal_newlines=True, shell=True)
        bios['release_date'] = subprocess.check_output("dmidecode --string bios-release-date", universal_newlines=True, shell=True)
        bios['version'] = subprocess.check_output("dmidecode --string bios-version", universal_newlines=True, shell=True)
    info['bios'] = bios

    # CPU
    cpu = dict(cpuinfo.get_cpu_info())
    cpu['processor'] = uname_result.processor
    cpu['cpu-times'] = psutil.cpu_times()
    cpu['pyhsical-core-count'] = psutil.cpu_count(False)
    cpu['logical-core-count'] = psutil.cpu_count(True)
    cpu['stats'] = psutil.cpu_stats()
    info['cpu'] = cpu

    # Memory
    memory = dict()
    memory['virtual_memory'] = dict(psutil.virtual_memory()._asdict())
    memory['swap_memory'] = dict(psutil.swap_memory()._asdict())
    devices = list()
    if sys.platform == 'win32':
        print('TODO')
    else:
        # tail omits the first unrelated lines.
        output = subprocess.check_output("dmidecode -t 17 | tail -n +5", universal_newlines=True, shell=True)
        dimm = dict()
        for line in str(output).splitlines():
            l = line.strip()
            if not l:
                devices.append(dimm)
                dimm = dict()
                continue
            if l.startswith('Type:'):
                dimm['type'] = l.replace("Type: ", "").strip().rstrip()
            if l.startswith('Size:'):
                dimm['size'] = l.replace("Size: ", "").strip().rstrip()
            if l.startswith('Speed:'):
                dimm['speed'] = l.replace("Speed: ", "").strip().rstrip()
            if l.startswith('Manufacturer:'):
                dimm['manufacturer'] = l.replace("Manufacturer: ", "").strip().rstrip()
        if dimm:
            devices.append(dimm)
    memory['devices'] = devices
    info['memory'] = memory

    # Disk
    disk = dict()
    disk['disk_partitions'] = psutil.disk_partitions()
    root_path = 'C:/' if sys.platform == 'win32' else '/'
    # total, used, free, percent
    disk['disk_usage'] = dict(psutil.disk_usage(root_path)._asdict())
    if sys.platform == 'win32':
        print('TODO')
    else:
        output = subprocess.check_output("lshw -c disk -json", universal_newlines=True, shell=True)
        # lshw creates an invalid json, here we fix this output.
        # (somehow forgets adding comma between json elements and also forgets wrapping json elements in an array!)
        output_fixed = "[" + re.sub('\s*(\}\s*\{)\s*', '},{', output) + "]"
        disk['devices'] = json.loads(output_fixed)
    info['disk'] = disk

    # GPU
    gpu = dict()
    devices = list()
    if sys.platform == 'win32':
        print('TODO')
    else:
        output = subprocess.check_output(r"lspci | grep ' VGA ' | cut -d' ' -f1 | xargs -i sudo lspci -v -s {} "
                                      r"| tail -n +2", universal_newlines=True, shell=True)
        dev = dict()
        for line in str(output).splitlines():
            l = line.strip()
            if not l:
                devices.append(dev)
                dev = dict()
                continue
            if l.startswith('Subsystem:'):
                dev['subsystem'] = l.replace("Subsystem: ", "").strip().rstrip()
            if l.startswith('Memory') and ' prefetchable' in l:
                m = re.search('\[size=(.*)\]', l)
                dev['memory'] = m.group(1).strip()
            if l.startswith('Kernel modules:'):
                dev['kernel'] = l.replace("Kernel modules: ", "").strip().rstrip()
        if dev:
            devices.append(dev)
    gpu['devices'] = devices
    info['gpu'] = gpu

    # Network
    net = dict()
    net['connection'] = psutil.net_connections(kind='inet')
    net_if_addrs = psutil.net_if_addrs()
    net['interface_addresses'] = net_if_addrs
    mac_addresses = list()
    ip_addresses = list()
    for key in net_if_addrs:
        for snic in net_if_addrs[key]:
            if snic.family == socket.AF_INET:
                ip_addresses.append(snic.address)
            elif snic.family == psutil.AF_LINK:
                mac_addresses.append(snic.address)
    net['ip_addresses'] = ip_addresses
    net['mac_addresses'] = mac_addresses
    if sys.platform == 'win32':
        print('TODO')
    else:
        output = subprocess.check_output("lshw -c network -json", universal_newlines=True, shell=True)
        # lshw creates an invalid json, here we fix this output.
        # (somehow forgets adding comma between json elements and also forgets wrapping json elements in an array!)
        output_fixed = "[" + re.sub('\s*(\}\s*\{)\s*', '},{', output) + "]"
        net['devices'] = json.loads(output_fixed)
    info['network'] = net

    # Peripherals (USB connected devices)
    devices = []
    if sys.platform == 'win32':
        print('TODO')
    else:
        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb", universal_newlines=True)
        for i in df.split('\n'):
            if i:
                _inf = device_re.match(i)
                if _inf:
                    dinfo = _inf.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)
    info['peripheral_devices'] = devices

    # Installed packages/softwares
    installed_packages = list()
    if sys.platform == 'win32':
        output = subprocess.check_output(r"powershell.exe -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "
                                   r"Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* "
                                   r"| Select-Object -ExpandProperty DisplayName",
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
        output = subprocess.check_output(r"dpkg-query -f '${binary:Package} ${Version}\n' -W",
                                   universal_newlines = True, shell = True)
    installed_packages.extend([{"name": p.split()[0], "version": p.split()[1]}
                               for p in str(output).strip().split('\n')])
    info['installed_packages'] = installed_packages

    # Users
    users = []
    for user in psutil.users():
        if str(user[0]) is not 'None' and user[0] not in users:
            users.append(user[0])
    info['users'] = users

    # For debug purposes
    #pp.pprint(info)

    with open(System.Agent.sys_out_path(), 'w') as f:
        f.write(json.dumps(info))


if __name__ == '__main__':
    # Agent needs Python version 3.5!
    assert sys.version_info >= (3,5)
    collect()
