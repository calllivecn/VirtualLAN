#!/usr/bin/env python3
#coding=utf-8

TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

Buffer=65535

write_size=65535

read_size=2048

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

data = s.recv(Buffer)

tun=tun_create(if_name='tun0',ipaddress='{}/24'.format(socket.inet_ntoa(data)))
fd=tun.fileno()

def tun_recv():
	
	cache=b''
	
	def Recv():
		nonlocal cache
		cache += s.recv(Buffer)
		if cache == b'':
			raise KeyboardInterrupt('server exit!')
		
	try:

		while 1:
			if cache == b'':
				Recv()

			length,cache = struct.unpack('!H',cache[0:2])[0],cache[2:]
			
			if cache ==b'':
				Recv()

			print('data length ',length)
			if length <= len(cache):
				data,cache = cache[0:length],cache[length:]
				os.write(fd,data)
			else:
				while length > len(cache):
					Recv()
				data,cache = cache[0:length],cache[length:]
				os.write(fd,data)

	except KeyboardInterrupt:
			exit(-1)
	finally:
		s.close()

def tun_send():
	while 1:
		data = os.read(fd,read_size)
		length=len(data)
		#print(socket.inet_ntoa(data[12:16]),'-->',socket.inet_ntoa(data[16:20]))
		print('os.read data size',len(data))
		data=struct.pack('!H',length)+data
		send_count = s.send(data)
		print('sned size',send_count)
		if send_count != len(data):
			print('Error send :','send size',send_count,'data size',len(data))

try:
	th=threading.Thread(target=tun_recv,daemon=1)
	th.start()
	tun_send()
except (KeyboardInterrupt,OSError):
	print('tun0 exit...')
finally:
	s.close()
