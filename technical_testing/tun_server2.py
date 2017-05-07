#!/usr/bin/env python3
#coding=utf-8



ADDR = ''

PORT = 6789

READ_BUF = 4096

IP_PKG_FORWARD_SIZE = 128


import socket
from time import ctime,time
from queue import Queue
from struct import pack,unpack
from threading import Thread
from selectors import DefaultSelector,EVENT_READ,EVENT_WRITE
from multiprocessing import Process,Pipe


sock_dict={}

unuse_ip=[ '172.16.10.'+str(x) for x in range(1,255) ]

use_ip=[]

pkg_recv = Queue(IP_PKG_FORWARD_SIZE)

pkg_forward = Queue(IP_PKG_FORWARD_SIZE)


selector = DefaultSelector()


def add_virtual_net(Sock):
	add_ip = unuse_ip.pop(0)
	sock_dict[add_ip] = Sock
	Sock.conn.send(socket.inet_aton(add_ip))
	use_ip.append(add_ip)

	selector.register(Sock.conn,EVENT_READ) 
	re_code = Sock.conn.recv(READ_BUF)
	
	if re_code == b'ok':
		return 'ok'
	else:
		return 'err'


class SockRecvQueue:
	'''socket 接收队列'''
	
	cache = b''

	def __init__(self,conn):
		self.conn=conn
	
	def recv_pkg(self):
		sock = self.conn
		cache = self.cache

		def Recv():
			nonlocal cache
			cache += sock.recv(READ_BUF)
			if cache == b'':
				return 'server exit!'
				
		while True:
			if cache == b'':
				re_code = Recv()
				if re_code == 'server exit!':
					return 'err'
				
			length = unpack('!H',cache[0:2])[0]
			data = cache[0:2]
	
			if cache ==b'':
				Recv()
	
			#print('data length ',length)
			if length <= len(cache):
				data += cache[0:length]
				cache = cache[length:]
				#osock.write(fd,data)
				return data
			else:
				while length > len(cache):
					Recv()
				data += cache[0:length]
				cache = cache[length:]
				#osock.write(fd,data)
				return data

def recv_select():
	event_list = selector.select()
	for key, event in event_list:
		conn = key.fileobj

		if event == EVENT_READ:
			print('recv_select() event 是读取事件')
			pkg = recv_pkg(conn)
			print('recv_pkg() ... done')
			if pkg != 'err':
				pkg_recv.put(pkg)
			else:
				selector.unregister(conn)
				print('recv_pkg() --> err')
				
		else:
			pass


def ip_pkg_forward():
	
	pkg = pkg_recv.get()
	print('收到 pkg 包')
	src,dst = pkg[12:16] ,pkg[16:20] # 源地址 ，目的地址

	if dst in sock_dict: ### and src in sock_dict:
		sock_dict[dst].conn.send(pkg)
	else:
		print('目的{}不可达'.format(socket.inet_ntoa(dst)))
	


'''
def LAN_forward(sock)
	selector = DefaultSelector()
	selector.register(sock,EVENT_READ)
	
	cache = b'' # recv_pkg() 缓存

	while True:
		event_list = selector.select()

		for key , event in event_list:
			conn = key.fileobj
			if event == EVENT_READ:
				data = recv_pkg(sock)
			elif event == EVENT_WRITE:
				pass
			else:
				pass
'''


def work():

	server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
	server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
	server_sock.bind((ADDR,PORT))

	server_sock.listen(128)
	
	#selector = selectors.DefaultSelector()
	#selector.register(server_sock,selectors.EVENT_READ)

	pkg_recv_th = Thread(target=recv_select)
	pkg_recv_th.start()

	ip_pkg_forward_th = Thread(target=ip_pkg_forward)
	ip_pkg_forward_th.start()


	while True:
		
		sock, addr = server_sock.accept()
		print('{} : {}:{} 已连接'.format(ctime(),*addr))
		add_virtual_net(sock)

		

work()
