from ctypes import Structure, Union, byref, addressof, c_char, c_wchar, c_char_p, c_ubyte, c_short, c_ushort, c_int, c_ulong, ARRAY, POINTER, pointer


class sockaddr(Structure):
    _fields_ = [('sa_family', c_ushort),
                ('sa_data', ARRAY(c_char, 14))]


class ifa_ifu(Union):
    _fields_ = [('ifu_broadaddr', sockaddr),
                ('ifu_dstaddr', sockaddr)]


class ifaddr(Structure):
    pass


'''
ifaddr._fields_=[('ifa_addr',sockaddr),
				('ifa_ifu',ifa_ifu),
				('iface',None),
				('ifaddr',POINTER(ifaddr))]
'''


class ifmap(Structure):
    _fields_ = [('mem_start', c_ulong),
                ('mem_end', c_ulong),
                ('base_addr', c_ushort),
                ('irq', c_ubyte),
                ('dma', c_ubyte),
                ('port', c_ubyte)]


class ifr_ifrn(Union):
    _fields_ = [('ifrn_name', ARRAY(c_char, 16))]


class ifr_ifru(Union):
    _fields_ = [('ifru_addr', sockaddr),
                ('ifru_dstaddr', sockaddr),
                ('ifru_broadaddr', sockaddr),
                ('ifru_netmask', sockaddr),
                ('ifru_hwaddr', sockaddr),
                ('ifru_flags', c_short),
                ('ifru_ivalue', c_int),
                ('ifru_mtu', c_int),
                ('ifru_map', ifmap),
                ('ifru_slave', ARRAY(c_char, 16)),
                ('ifru_newname', ARRAY(c_char, 16)),
                ('ifru_data', c_char_p)]


class ifreq(Structure):
    _fields_ = [('ifr_ifrn', ifr_ifrn), ('ifr_ifru', ifr_ifru)]


class ifc_ifcu(Union):
    _fields_ = [('ifcu_buf', c_char_p),
                ('ifcu_req', POINTER(ifreq))]


class ifconf(Structure):
    _fields_ = [('ifc_len', c_int),
                ('ifc_ifcu', ifc_ifcu)]
