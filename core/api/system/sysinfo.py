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
#from core.api.system.system import System

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
        p = subprocess.Popen("powershell.exe -NoProfile -InputFormat None -ExecutionPolicy Bypass "
                             "-Command \"Get-WmiObject win32_bios "
                             "| Format-Table Manufacturer, @{Label='v'; Expression={'#SEP#' + $_.Version}} "
                             "-HideTableHeaders\"",
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, _ = p.communicate()
        parts = output.strip().split('#SEP#')
        bios['version'] = str(parts[-1])
        bios['vendor'] = " ".join(parts[:-1])
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
        p = subprocess.Popen("powershell.exe -NoProfile -InputFormat None -ExecutionPolicy Bypass "
                             "-Command \"Get-WmiObject  win32_physicalmemory "
                             "| Format-Table Manufacturer,Configuredclockspeed,MemoryType,Capacity -HideTableHeaders\"",
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, _ = p.communicate()
        for line in str(output).strip().splitlines():
            l = line.strip()
            if not l:
                continue
            dimm = dict()
            parts = l.split()
            # size in mb
            dimm['size'] = str(int(parts[-1]) // (1024*1024))
            dimm['type'] = 'DDR3' if int(parts[-2]) == 24 else ('DDR2' if int(parts[-2]) == 21 else 'DDR')
            dimm['speed'] = str(parts[-3])
            dimm['manufacturer'] = " ".join(parts[:-3])
            devices.append(dimm)
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
                dimm['type'] = l.replace("Type: ", "").strip()
            if l.startswith('Size:'):
                dimm['size'] = l.replace("Size: ", "").strip()
            if l.startswith('Speed:'):
                dimm['speed'] = l.replace("Speed: ", "").strip()
            if l.startswith('Manufacturer:'):
                dimm['manufacturer'] = l.replace("Manufacturer: ", "").strip()
        if dimm:
            devices.append(dimm)
    memory['devices'] = devices
    info['memory'] = memory

    # Disk
    disk = dict()
    disk['disk_partitions'] = [dict(p._asdict()) for p in psutil.disk_partitions()]
    root_path = 'C:/' if sys.platform == 'win32' else '/'
    # total, used, free, percent
    disk['disk_usage'] = dict(psutil.disk_usage(root_path)._asdict())
    if sys.platform == 'win32':
        """
        cmd = 'get-disk | where-object -filterscript {$_.BusType -Eq "SATA"} | Select-Object ' \
              '@{Name="F"; Expression = {"#DESC#" + $_.FriendlyName + "#DESC#"}},' \
              '@{Name="V"; Expression = {"#VER#" + $_.FirmwareVersion + "#VER#"}},' \
              '@{Name="S"; Expression = {"#SER#" + $_.SerialNumber + "#SER#"}},' \
              '@{Name="P"; Expression = {"#PRO#" + $_.Model + "#PRO#"}},' \
              '@{Name="M"; Expression = {"#VEN#" + $_.Manufacturer + "#VEN#"}} | Format-Table -HideTableHeaders'
        print(cmd)
        p = subprocess.Popen(r"$command=" + cmd + r";$bytes = [System.Text.Encoding]::Unicode.GetBytes($command);$encodedCommand = [Convert]::ToBase64String($bytes);powershell.exe -encodedCommand $encodedCommand",
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        """
        cmd = r'get-disk | where-object -filterscript {$_.BusType -Eq "SATA"} | Select-Object ' \
              '@{Name="F"; Expression = {"#DESC#" + $_.FriendlyName + "#DESC#"}},' \
              '@{Name="V"; Expression = {"#VER#" + $_.FirmwareVersion + "#VER#"}},' \
              '@{Name="S"; Expression = {"#SER#" + $_.SerialNumber + "#SER#"}},' \
              '@{Name="P"; Expression = {"#PRO#" + $_.Model + "#PRO#"}},' \
              '@{Name="M"; Expression = {"#VEN#" + $_.Manufacturer + "#VEN#"}} | Format-Table -HideTableHeaders'
        print(cmd)
        p = subprocess.Popen(r"$command=" + cmd + r";$bytes = [System.Text.Encoding]::Unicode.GetBytes($command);$encodedCommand = [Convert]::ToBase64String($bytes);powershell.exe -encodedCommand $encodedCommand",
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = p.communicate()
        devices = list()
        regex = re.compile('#DES#(.*)#DES#.*#VER#(.*)#VER#.*#SER#(.*)#SER#.*#PRO#(.*)#PRO#.*#VEN#(.*)#VEN#')
        for line in str(output).strip().splitlines():
            l = line.strip()
            if not l:
                continue
            dev = dict()
            m = regex.match(l)
            if not m:
                continue
            dev['description'] = m.group(1) if m.group(1) is not None else ''
            dev['version'] = m.group(2) if m.group(2) is not None else ''
            dev['serial'] = m.group(3) if m.group(3) is not None else ''
            dev['product'] = m.group(4) if m.group(4) is not None else ''
            dev['vendor'] = m.group(5) if m.group(5) is not None else ''
            devices.append(dev)
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
    #net['connection'] = psutil.net_connections(kind='inet')
    net_if_addrs = psutil.net_if_addrs()
    net['interface_addresses'] = [{"inet": str(key), "addr": [dict(addr._asdict()) for addr in value]} for key, value in net_if_addrs.items()]
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
        p = subprocess.Popen("powershell.exe -NoProfile -InputFormat None -ExecutionPolicy Bypass "
                                         "-Command \"Get-ItemProperty -Name DisplayName -ErrorAction SilentlyContinue "
                                         "HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* "
                                         "| Format-Table -HideTableHeaders -Property DisplayName\"",
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, _ = p.communicate()
    else:
        output = subprocess.check_output(r"dpkg-query -f '${binary:Package} ${Version}\n' -W",
                                   universal_newlines=True, shell=True)
    installed_packages.extend([{"name": p.split()[0] if sys.platform != 'win32' else p.strip().rstrip(),
                                "version": p.split()[1] if sys.platform != 'win32' else ''}
                               for p in str(output).strip().splitlines()])
    info['installed_packages'] = installed_packages

    # Users
    users = []
    for user in psutil.users():
        if str(user[0]) is not 'None' and user[0] not in users:
            users.append(user[0])
    info['users'] = users

    # For debug purposes
    pp.pprint(info)

    #with open(System.Agent.sys_out_path(), 'w') as f:
    #    f.write(json.dumps(info))


if __name__ == '__main__':
    # Agent needs Python version 3.5!
    assert sys.version_info >= (3,5)
    collect()
