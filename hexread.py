# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 23:12:45 2013

@author: Nathan
"""
from ctypes import *


MsgDataType = c_uint8 * 8

msg = MsgDataType()
msg[0] = 23
msg[1] = 45

f = open("test1.a00", "r")
w = open("write.txt", "w")
f.next()        

for s in f:
    a = s.split()
    b = s.split()
    a.reverse()
    while(len(a) > 0):
        i = a.pop()
        if i == '\x03':
            break
        j = a.pop()
        w.write(repr(int(i,16)) + " " + repr(int(j,16)) + '\n')
        
w.flush()
print 'done'