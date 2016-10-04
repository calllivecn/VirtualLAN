#!/usr/bin/env python3
#coding=utf-8

import socket,struct


server_addr=('192.168.10.2',6789)

def str_to_byte(addr):
        return socket.inet_aton(addr[0])+struct.pack('!H',addr[1])

def byte_to_str(byte):
        return (socket.inet_ntoa(byte[0:4]),struct.unpack('!H',byte[4:6])[0])


sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

sock.connect(server_addr)


data = byte_to_str(sock.recv(1024))
print('接收到 B : ',data)

local_sock = sock.getsockname()
sock.close()

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
try:
	sock.bind(local_sock)	
	sock.connect(data)
	sock.close()
except socket.error:
	print('connect ...')


print('创建socket 等待B 连接。。。')

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

print('bind local_sock')
sock.bind(local_sock)	
print('listen ...')
sock.listen(1)

print('accept...')
client_B , addr_B = sock.accept()

print('client_B info :',addr_B)


while 1:
	try:
		data = client_B.recv(1024)
		print('recv : ',data.decode())
		if data.decode() == 'quit':
			break
	except KeyboradInterrupt:
		print('exit ...')
		exit(0)

client_B.close()
sock.close()

