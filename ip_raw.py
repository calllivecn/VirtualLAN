#!/usr/bin/env python3
#coding=utf-8

import socket

#sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_UDP)
sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW|socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
while 1:
	try:
		data , addr = sock.recvfrom(65536)
		ip = socket.inet_ntoa(data[12:16])
		print('测ip address {}\t实 ip {}'.format(ip,addr))
		
	except KeyboardInterrupt:
		sock.close()
		break
