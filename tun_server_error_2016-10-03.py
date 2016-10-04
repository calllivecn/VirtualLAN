#!/usr/bin/env python3
#coding=utf-8

TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

import os,fcntl,subprocess,socket,struct,multiprocessing,queue,threading

sock_dict={}
sock_dict_lock=threading.Lock()

def tun_create(if_name,ipaddress='172.16.10.1/24',brd='172.16.10.255',gateway='',owner=0):
	print('ipaddress -->',ipaddress,'brd -->',brd)
	tun = open('/dev/net/tun','r+b',buffering=0)
	ifr = struct.pack('16sH',if_name.encode(),IFF_TUN | IFF_NO_PI)
	fcntl.ioctl(tun,TUNSETIFF,ifr)
	fcntl.ioctl(tun,TUNSETOWNER,owner)
	subprocess.check_call('ip link set dev {} up'.format(if_name),shell=1)
	subprocess.check_call('ip addr add dev {} {} brd {}'.format(if_name,ipaddress,brd),shell=1)
	if gateway != '':
		subprocess.check_call('ip route change {} via {}'.format(ipaddress,gateway),shell=1)
	return tun


def accept_access():
	global sock_dict
	sock = socket.socket()
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sock.bind(('0.0.0.0',6789))
	sock.listen(5)
#	while 1:
	client,addr = sock.accept()
	source_addr = socket.inet_aton('172.16.10.100')
	client.send(source_addr)
	with sock_dict_lock:
			sock_dict[source_addr]=client
		
	client,addr = sock.accept()
	source_addr = socket.inet_aton('172.16.10.101')
	client.send(source_addr)
	with sock_dict_lock:
			sock_dict[source_addr]=client


tun = tun_create('tun0')
fd = tun.fileno()
accept_access()
for k,v in zip(sock_dict.keys(),sock_dict.values()):
	print(k,v)

try:
	while 1:
		data = os.read(fd,2048)
		print('os.read --> ok')
		destination = data[16:20]
		print(socket.inet_ntoa(destination))
		if destination in sock_dict:
			sock_dict[destination].send(data)
		else:
			print('error -->',socket.inet_ntoa(destination))
except KeyboardInterrupt:
	print('exit...')

finally:
	for client in sock_dict.values():
		client.close()
