#!/usr/bin/env python3
#coding=utf-8


ADDR = ''

PORT = 6789

READ_BUF = 4096

import socket,selectors
from multiprocessing import Process,Pipe


sock_dict={}

unuse_ip=[ '172.16.10.'+str(x) for x in range(1,254)]

use_ip=[]

def add_virtual_net(sock):
	add_ip = unuse_ip.pop(0)
	sock.send(socket.inet_aton(add_ip))
	re_code = sock.read(READ_BUF)
	if re_code == b'ok':
		return 'ok'
	else:
		return 'err'
def recv_pkg(sock)
	


def ip_pkg_forward(pkg):
	
	src,dst = pkg[12:16] ,pkg[16:20] # 源地址 ，目的地址

	if dst in sock_dict: ### and src in sock_dict:
		sock_dict[dst].send(pkg)
	else:
		print('目的{}不可达'.format(socket.inet_ntoa(dst)))
	
	

def work():

	server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
	server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
	server_sock.bind((ADDR,PORT))

	server_sock.listen(128)
	
	selector = selectors.DefaultSelector()
	selector.register(server_sock,selectors.EVENT_READ)

	while True:
		sock, addr = server_sock.accept()
		add_virtual_net(sock)
		

		



