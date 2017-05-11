#!/usr/bin/env python3
#coding=utf-8


import struct,socket,array,fcntl,sys


class NetworkError(Exception):
	pass

def _get_interface_list():
	"""Provides a list of available network interfaces
	as a list of tuples (name, ip)"""
	max_iface = 32 # Maximum number of interfaces(Aribtrary)
	byte_s = max_iface * 32
	is_32bit = (8 * struct.calcsize("P")) == 32 # Set Architecture
	struct_size = 32 if is_32bit else 40

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		names = array.array('B', bytes(byte_s))
		outbytes = struct.unpack('iL', fcntl.ioctl(
		s.fileno(),
		0x8912, # SIOCGIFCONF
		struct.pack('iL', byte_s, names.buffer_info()[0])
		))[0]
		namestr =  names.tostring()
		return [( namestr[i:i + 32].split(bytes(1), 1)[0],
			socket.inet_ntoa(namestr[i + 20:i + 24]))
			for i in range(0, outbytes, struct_size)]
		
	except IOError:
		raise NetworkError('Unable to call ioctl with SIOCGIFCONF')


def all_interfaces():
	'''
	Return all interfaces that are up
	'''
	is_64bits = sys.maxsize > 2**32
	struct_size = 40 if is_64bits else 32
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	max_possible = 8 # initial value
	while True:
		byte_s = max_possible * struct_size
		names = array.array('B', bytes(byte_s))
		outbytes = struct.unpack('iL', fcntl.ioctl(
		s.fileno(),
		0x8912, # SIOCGIFCONF
		struct.pack('iL', byte_s, names.buffer_info()[0])
		))[0]
		if outbytes == byte_s:
			max_possible *= 2
		else:
			break
	namestr = names.tostring()
	return [(namestr[i:i+16].split(bytes(1), 1)[0],
			socket.inet_ntoa(namestr[i+20:i+24]))
			for i in range(0, outbytes, struct_size)]


def get_ip_ifname(ifname):
	# > LOOK
	# You are in a maze of twisty passages, all alike.
	# > GO WEST
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
	# It is dark here. You are likely to be eaten by a grue.
	# > _
		return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915, # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
		)[20:24])
	except Exception:
		return None

def set_ip_ifname(ifname):
	is_64bit = sys.maxsize > 1<<32
	byte_s = 32*32
	
	struct_size = 40 if is_64bit else 32
	names = array.array('B',bytes(byte_s))
	
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	try:
		option = struct.pack('32sI',
								ifname[:32].encode(),
								struct.unpack('I',socket.inet_aton('172.16.10.2'))[0])
								#names.buffer_info()[0])
		print(option)
		result = fcntl.ioctl(s.fileno(),0x8916,option)
		outbytes = struct.unpack('iL',result[0])
		
		namestr = names.tostring()
		
		return namestr
	except Exception as e:
		print('异常')
		raise e

if __name__ == '__main__':
	set_ip_ifname('eth0')
	from pprint import pprint
	result = _get_interface_list()
	
	pprint(result)
	
	result = all_interfaces()
	
	pprint(result)
	
	result = get_ip_ifname('eth0')
	
	pprint(result)
