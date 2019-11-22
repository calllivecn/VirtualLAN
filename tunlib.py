
# 操作接口

SIOCADDRT=0x890B
SIOCDELRT=0x890C
SIOCRTMSG=0x890D
SIOCGIFNAME=0x8910
SIOCSIFLINK=0x8911
SIOCGIFCONF=0x8912
SIOCGIFFLAGS=0x8913
SIOCSIFFLAGS=0x8914
SIOCGIFADDR=0x8915
SIOCSIFADDR=0x8916
SIOCGIFDSTADDR=0x8917
SIOCSIFDSTADDR=0x8918
SIOCGIFBRDADDR=0x8919
SIOCSIFBRDADDR=0x891a
SIOCGIFNETMASK=0x891b
SIOCSIFNETMASK=0x891c
SIOCGIFMETRIC=0x891d
SIOCSIFMETRIC=0x891e
SIOCGIFMEM=0x891f
SIOCSIFMEM=0x8920
SIOCGIFMTU=0x8921
SIOCSIFMTU=0x8922
SIOCSIFNAME=0x8923
SIOCSIFHWADDR=0x8924
SIOCGIFENCAP=0x8925
SIOCSIFENCAP=0x8926
SIOCGIFHWADDR=0x8927
SIOCGIFSLAVE=0x8929
SIOCSIFSLAVE=0x8930
SIOCADDMULTI=0x8931
SIOCDELMULTI=0x8932
SIOCGIFINDEX=0x8933
SIOGIFINDEX=SIOCGIFINDEX
SIOCSIFPFLAGS=0x8934
SIOCGIFPFLAGS=0x8935
SIOCDIFADDR=0x8936
SIOCSIFHWBROADCAST=0x8937
SIOCGIFCOUNT=0x8938
SIOCGIFBR=0x8940
SIOCSIFBR=0x8941
SIOCGIFTXQLEN=0x8942
SIOCSIFTXQLEN=0x8943
SIOCDARP=0x8953
SIOCGARP=0x8954
SIOCSARP=0x8955
SIOCDRARP=0x8960
SIOCGRARP=0x8961
SIOCSRARP=0x8962
SIOCGIFMAP=0x8970
SIOCSIFMAP=0x8971
SIOCADDDLCI=0x8980
SIOCDELDLCI=0x8981
SIOCDEVPRIVATE=0x89F0
SIOCPROTOPRIVATE=0x89E0

IFF_UP = 0x1

RTF_UP = 0x0001
RTF_HOST = 0x0004
RTF_REJECT = 0x0200


# 操作 /dev/net/tun 
TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

TUN_DEV_FILE='/dev/net/tun'


import sys,os
from socket import socket,AF_INET,SOCK_DGRAM,inet_ntoa,inet_aton
from fcntl import ioctl
from struct import pack,unpack
from array import array

def get_iface_list():
	max_iface = 32
	byte_s = max_iface *32
	is64bit = sys.maxsize > 1<<32
	struct_size = 40 if is64bit else 32
	
	try:
		s = socket(AF_INET,SOCK_DGRAM)
		names = array('B',bytes(byte_s))
		op = pack('iL',byte_s,names.buffer_info()[0])
		result = ioctl(s.fileno(),0x8912,op)
		outbytes = unpack('iL',result)[0]
		namestr = names.tostring()
		iface_ip=[]
		for i in range(0,outbytes,struct_size):
			iface_ip.append(namestr[i:i+32].split(bytes(1),1)[0].decode())
			iface_ip.append(inet_ntoa(namestr[i+20:i+24]))
	except OSError as e:
		raise e

	return iface_ip

def get_ip_ifname(ifname):
		s = socket(AF_INET,SOCK_DGRAM)
		try:
			ifr = pack('32s','eth0'.encode())
			result = ioctl(s.fileno(),0x8915,(ifr))
			print(inet_ntoa(result[20:24]))
		finally:
			pass

def set_ip_ifname(ifname,ip,netmask):
		s = socket(AF_INET,SOCK_DGRAM)
		try:
			ifr = pack('16sH14s',ifname.encode(),AF_INET,bytes(2)+inet_aton(ip))
			result = ioctl(s.fileno(),0x8916,(ifr))
			ifr = pack('16sH14s',ifname.encode(),AF_INET,bytes(2)+inet_aton(netmask))
			result = ioctl(s.fileno(),0x891c,(ifr))
		except OSError as e:
			raise e

def add_route(ifname,dst_ip,gateway,mask):
	s = socket(AF_INET,SOCK_DGRAM)
	op = pack('LH14sH14sH14sH46s',0,
				AF_INET,bytes(2)+inet_aton(dst_ip),
				AF_INET,bytes(2)+inet_aton(gateway),
				AF_INET,bytes(2)+inet_aton(mask),
				RTF_UP | RTF_HOST | RTF_REJECT,
				bytes(1))
	ioctl(s.fileno(),0x890B,op)

def del_route(dst_ip,gateway,mask):
	s = socket(AF_INET,SOCK_DGRAM)
	
	op = pack('LH14sH14sH14sH46s',0,
				AF_INET,bytes(2)+inet_aton(dst_ip),
				AF_INET,bytes(2)+inet_aton(gateway),
				AF_INET,bytes(2)+inet_aton(mask),
				RTF_UP | RTF_HOST | RTF_REJECT,
				bytes(1))
	ioctl(s.fileno(),0x890c,op)



def up_iface(ifname):
	s = socket(AF_INET,SOCK_DGRAM)
	try:
		op = pack('16sh',ifname.encode(),0)
		status = ioctl(s.fileno(),0x8913,op)
		status = unpack('16sh',status)[1]
		ifr = pack('16sh',ifname.encode(),status | IFF_UP)
		result = ioctl(s.fileno(),0x8914,ifr)
	except OSError as e:
		raise e

def __check_ifname(ifname='tun'):
	i=0
	iface_ip = get_iface_list()
	while ifname+str(i) in iface_ip:
		if i > 99999:
			return False
		i+=1
	return ifname+str(i)

def tun_create():
	'''返回 create (tun_name,tun_file_object)'''
	ifname = __check_ifname()
	ifr = pack('16sH',ifname.encode(),IFF_TUN | IFF_NO_PI)
	tun = open(TUN_DEV_FILE,'r+b',buffering=0)
	ioctl(tun,TUNSETIFF,ifr)
	ioctl(tun,TUNSETOWNER,0)

	return ifname,tun


def mask(netmask=24):
	mask = 0
	for i in range(32 - netmask,32):
		mask = mask | 1<<i
	
	return inet_ntoa(pack('!I',mask))

def ip_add_route(gw,mask,dst='0.0.0.0'):
	subprocess.check_call('ip route add {}/{} via {}'.format(dst,mask,gw))

def ip_del_route(gw,mask,dst='0.0.0.0'):
	subprocess.check_call('ip route del {}/{} via {}'.format(dst,mask,gw))

def tun_active(ifname,ip,netmask=24):
	up_iface(ifname)
	set_ip_ifname(ifname,ip,mask(netmask))

if __name__ == '__main__':
	#add_route('0.0.0.0','10.0.0.254',mask(24))
	#del_route('0.0.0.0','10.0.0.254',mask(32))


	ifname , tun = tun_create()
	tun_active(ifname,'10.0.0.1',24)
	fd = tun.fileno()
	try:
		while True:
			data = os.read(fd,65535)
			print(data)
	except KeyboardInterrupt:
		print('exit...')
	finally:
	#input('pause...')
		tun.close()
