#!/usr/bin/env python3
#coding=utf-8

import socket

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("123.45.67.89", 30000))
sock.listen(5)

conn1, addr1 = sock.accept()
conn1_info = addr1[0] + "|" + str(addr1[1]) + "|0"
conn1.sendall("#你已连接上,请等待另一名用户\n".encode())
conn2, addr2 = sock.accept()
conn2_info = addr2[0] + "|" + str(addr2[1]) + "|1"
conn2.sendall("#你已连接上,另一名用户已就绪\n".encode())

conn1.sendall(conn2_info.encode())
conn2.sendall(conn1_info.encode())

conn1.close()
conn2.close()
sock.close()
