#!/usr/bin/env python3
#coding=utf-8


import os
from time import sleep
import struct
import socket

def p2p_connect(local_address, local_port, send_file_path, recv_folder_path,server_address,server_port):
    if not os.path.exists(send_file_path):
        raise FileNotFoundError(send_file_path)
    if not os.path.exists(recv_folder_path):
        os.mkdirs(recv_folder_path)  # 若为windows 只有mkdir
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((local_address, local_port))
    sock.connect((server_address, server_port))
    rcv_msgs = sock.recv(1024).decode()
    while rcv_msgs.startswith("#"):
        print(rcv_msgs)
        rcv_msgs = sock.recv(1024).decode()
    rcv_msgs = rcv_msgs.split("|")
    remote_addr = rcv_msgs[0]
    remote_port = int(rcv_msgs[1])
    is_server = rcv_msgs[2] == "0"
    print(rcv_msgs)
    sock.close()

    if is_server:
        try_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # 打孔
        try_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try_conn.bind((local_address, local_port))
        try_conn.connect_ex((remote_addr, remote_port))
        try_conn.close()
        recv_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recv_sock.bind((local_address, local_port))
        recv_sock.listen(1)
        conn, addr = recv_sock.accept()
        conn.sendall(os.path.split(send_file_path)[1].encode())  # 发送文件名
        with open(send_file_path, "rb") as f:
            size = os.path.getsize(send_file_path)
            print("共发送", size, "字节")
            conn.sendall(struct.pack(">I", size))  # 发送文件大小
            data = f.read(1024)
            while data:
                conn.sendall(data)
                data = f.read(1024)
            conn.sendall("")
        conn.close()
        recv_sock.close()
    else:
        conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        while conn.connect_ex((remote_addr, remote_port)) != 0:  # 注意网络情况，可能为死循环
            sleep(1)
        file_name = conn.recv(1024).decode()  # 接收文件名
        size = struct.unpack(">I", conn.recv(1024))[0]  # 接收文件大小
        print("接收 : ", file_name, "  (", size, "bytes)")
        with open(os.path.join(recv_folder_path,file_name), "wb") as f:
            count = 0
            data = conn.recv(1024)
            print("\r已完成 : {:.0f}%".format(count / size*100), end="", flush=True)
            while data:
                f.write(data)
                length = len(data)
                count += length
                print("\r已完成 : {:.0f}%".format(count / size*100), end="", flush=True)
                data = conn.recv(1024)
        print(" 传输完成")
        conn.close()

if __name__ == '__main__':
    name = socket.gethostname()
    local_port = 22000  # 本地端口
    local_address = socket.gethostbyname(name)  #本地地址
    file_path="text.xml"  # 待传输文件
    folder_path=""  # 接收文件文件夹
    remote_address="123.45.67.89"  # 服务器地址
    remote_port=30000  # 服务器端口
    p2p_connect(local_address,local_port,file_path,folder_path,remote_address,30000)
