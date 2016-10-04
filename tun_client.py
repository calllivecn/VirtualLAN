#!/usr/bin/env python3
#coding=utf-8

TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

import os,fcntl,socket,struct,subprocess,threading

def tun_create(if_name,ipaddress='172.16.10.1/24',brd='172.16.10.255',gateway='',owner=0):
    tun = open('/dev/net/tun','r+b',buffering=0)
    ifr = struct.pack('16sH',if_name.encode(),IFF_TUN | IFF_NO_PI)
    fcntl.ioctl(tun,TUNSETIFF,ifr)
    fcntl.ioctl(tun,TUNSETOWNER,owner)
    subprocess.check_call('ip link set dev {} up'.format(if_name),shell=1)
    subprocess.check_call('ip addr add dev {} {} brd {}'.format(if_name,ipaddress,brd),shell=1)
    if gateway != '':
        subprocess.check_call('ip route change {} via {}'.format(ipaddress,gateway),shell=1)
    return tun


address=('192.168.10.2',6789)

s=socket.socket()

s.connect(address)

data = s.recv(2048)

tun=tun_create(if_name='tun0',ipaddress='{}/24'.format(socket.inet_ntoa(data)))
fd=tun.fileno()

def tun_recv():
	while 1:
		data=s.recv(2048)
		#print(socket.inet_ntoa(data[12:16]),'-->',socket.inet_ntoa(data[16:20]))
		os.write(fd,data)

th = threading.Thread(target=tun_recv,daemon=1)
th.start()

try:
	while 1:
		user_data = os.read(fd,2048)
		#print(socket.inet_ntoa(data[12:16]),'-->',socket.inet_ntoa(data[16:20]))
		s.send(user_data)

except KeyboardInterrupt:
	print('tun0 exit...')
finally:
	s.close()



