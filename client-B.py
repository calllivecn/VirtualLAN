#!/usr/bin/env python3
#coding=utf-8

import socket,struct,time


server_addr=('192.168.10.2',6789)

def str_to_byte(addr):
        return socket.inet_aton(addr[0])+struct.pack('!H',addr[1])

def byte_to_str(byte):
        return (socket.inet_ntoa(byte[0:4]),struct.unpack('!H',byte[4:6])[0])


sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

sock.connect(server_addr)


data = byte_to_str(sock.recv(1024))

print('接收到 A : ',data)
local_sock = sock.getsockname()
sock.close()

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

time.sleep(3)

sock.bind(local_sock)

sock.connect(data)

print('client_A info :',sock.getpeername())

while 1:
	data = input('P2P >>> ')
	sock.send(data.encode())
	if data == 'quit':
		break

sock.close()

