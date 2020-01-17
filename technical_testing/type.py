
from ctypes import Structure, CDLL, POINTER, pointer, c_int, c_uint, c_char, c_char_p, c_float, c_ulong


class t(Structure):
    _fields_ = [('I', c_uint),
                ('f', c_float),
                ('c', c_char_p),
                ('L', c_ulong)]


t_e = t()

t_e.I = c_uint(1)
t_e.f = c_float(1.5)
t_e.c = c_char_p('哈哈成功了。。。'.encode())
t_e.L = c_ulong(1 << 40)

type_func = CDLL('./libtype.so')

type_func.run1.restype = c_int

return_i = type_func.run1(t_e)

print('run1() 的返回值 ：', return_i)

print(c_char*10)


return_i = type_func.run2(pointer(t_e))

print('run2() 的返回值 ：', return_i)

print('run2() 之后的t_e', t_e.f)
