#!/usr/bin/env python3
#coding=utf-8

import fcntl,subprocess,socket,struct,multiprocessing,queue,threading

sock_dict={}
sock_dict_lock=threading.Lock()

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

accept_access()
for k,v in zip(sock_dict.keys(),sock_dict.values()):
	print(k,v)

def router(source,dest):
	global sock_dict
	while 1:
		data=sock_dict[source].recv(2048)
		if data == b'':
			with sock_dict_lock:
				sock_dict.pop(source)
			break
		print(socket.inet_ntoa(source),'-->',socket.inet_ntoa(dest))
		sock_dict[dest].send(data)


th1=threading.Thread(target=router,args=(socket.inet_aton('172.16.10.100'),socket.inet_aton('172.16.10.101')),daemon=1)
th2=threading.Thread(target=router,args=(socket.inet_aton('172.16.10.101'),socket.inet_aton('172.16.10.100')),daemon=1)
th1.start()
th2.start()

try:
	while 1:
		input()
except KeyboardInterrupt:
	print('\rexit...')

finally:
	for client in sock_dict.values():
		client.close()
