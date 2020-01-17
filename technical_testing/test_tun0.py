#!/usr/bin/env python3
# coding=utf-8


import os
import fcntl
import struct
import socket
import subprocess


TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

tun = open('/dev/net/tun', 'r+b', buffering=0)

ifr = struct.pack('8sH', b'tun0', IFF_TUN | IFF_NO_PI)

fcntl.ioctl(tun, TUNSETIFF, ifr)

subprocess.check_call('ip link set dev tun0 up', shell=1)
subprocess.check_call(
    'ip addr add 172.16.10.1/24 brd 172.16.10.255 dev tun0', shell=1)
fd = tun.fileno()
try:
    while 1:
        data = os.read(fd, 2048)
        print('head 4 byte', hex(struct.unpack('!I', data[0:4])[0]))
        print('os.read data size', len(data), 'destination ip :', socket.inet_ntoa(
            data[20:24]), 'source ip', socket.inet_ntoa(data[16:20]))
except KeyboardInterrupt:
    print('exit...')
    exit(0)

finally:
    tun.close()
