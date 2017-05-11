
import struct,socket,array,fcntl


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
		for i in range(0, int(outbytes), struct_size):
			ifname = namestr[i:i + 32].split(bytes(1), 1)[0]
			ip = socket.inet_ntoa(namestr[i + 20:i + 24])
		return ifname,ip
	except IOError:
		raise NetworkError('Unable to call ioctl with SIOCGIFCONF')


from pprint import pprint
result = _get_interface_list()

pprint(result)

