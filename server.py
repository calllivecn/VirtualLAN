#!/usr/bin/env python3
#coding=utf-8

import time,socket,threading,struct


listen_addr=('0.0.0.0',6789)

def str_to_byte(addr):
	return socket.inet_aton(addr[0])+struct.pack('!H',addr[1])

def byte_to_str(byte):
	return (socket.inet_ntoa(byte[0:4]),struct.unpack('!H',byte[4:6]))


#def th(sock):
#	sock.send()


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

sock.bind(listen_addr)

sock.listen(5)

list_addr=[]
while 1:
	try:
		sock_A,addr_A = sock.accept()

		sock_B,addr_B = sock.accept()
	
		sock_A.send(str_to_byte(addr_B))

		sock_B.send(str_to_byte(addr_A))
		print(addr_A,addr_B,sep='\t')
	except KeyboardInterrupt:
		print('exit...')
		break

sock_A.close()
sock_B.close()
sock.close()




