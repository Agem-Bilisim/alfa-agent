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

OUTPUT_FILE = 'sysinfo.json'

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
info['virtual_memory'] = dict(psutil.virtual_memory()._asdict())
info['swap_memory'] = dict(psutil.swap_memory()._asdict())

# Disk
info['disk_partitions'] = psutil.disk_partitions()
root_path = 'C:/' if sys.platform == 'win32' else '/'
# total, used, free, percent
info['disk_usage'] = dict(psutil.disk_usage(root_path)._asdict())

# GPU
if sys.platform == 'win32':
    print('TODO')
else:
    gpu = subprocess.check_output(r"lspci | grep ' VGA ' | cut -d' ' -f1 | xargs -i sudo lspci -v -s {}",
                               universal_newlines=True, shell=True)
info['gpu'] = gpu.strip()

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
    process = subprocess.Popen(r"powershell.exe -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "
                               r"Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* "
                               r"| Select-Object -ExpandProperty DisplayName",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
else:
    process = subprocess.Popen(r"dpkg-query -f '${binary:Package}\n' -W",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result_code = process.wait()
p_out = process.stdout.read().decode('utf-8')
p_err = process.stderr.read().decode('utf-8')
if result_code == 0:
    installed_packages.append(str(p_out).strip().split('\n'))
info['installed_packages'] = installed_packages

# Users
info['users'] = psutil.users()

# For debug purposes
#pp.pprint(info)

with open(OUTPUT_FILE, 'w') as f:
    f.write(json.dumps(info))
