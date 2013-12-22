#
# Calling CANLIB from Python
#
# Requires Python 2.5, or Python 2.3/2.4 with ctypes installed.
# Has been tested with Python 2.5.
# You can get ctypes here: http://starship.python.net/crew/theller/ctypes
#

from ctypes import *

# For sleep()
import time

hexfile = "Template.a00"
can_id = 5

# -------------------------------------------------------------------------
# dll initialization
# -------------------------------------------------------------------------
# Load canlib32.dll
canlib32 = windll.canlib32

# Load the API functions we use from the dll
canInitializeLibrary = canlib32.canInitializeLibrary
canOpenChannel = canlib32.canOpenChannel
canBusOn = canlib32.canBusOn
canBusOff = canlib32.canBusOff
canClose = canlib32.canClose
canWrite = canlib32.canWrite
canRead = canlib32.canRead
canGetChannelData = canlib32.canGetChannelData

# A few constants from canlib.h
canCHANNELDATA_CARD_FIRMWARE_REV = 9
canCHANNELDATA_DEVDESCR_ASCII = 26


# Define a type for the body of the CAN message. Eight bytes as usual.
MsgDataType = c_uint8 * 8

# Initialize the library...
canInitializeLibrary()

# ... and open channels 0 and 1. These are assumed to be on the same
# terminated CAN bus.
hnd1 = canOpenChannel(c_int(0), c_int(32))

# Go bus on
stat = canBusOn(c_int(hnd1))
if stat < 0: 
    print "canBusOn channel 1 failed: ", stat
    assert(0)

# Setup a message
msg = MsgDataType()

#open hex2000 file
f = open(hexfile, "r")
w = open("write.txt", "w")
f.next()

time.sleep(1)
for s in f:
    a = s.split()
    b = s.split()
    a.reverse()
    while(len(a) > 0):
        i = a.pop()
        if i == '\x03':
            break
        j = a.pop()
        msg[0] = int(i,16)
        msg[1] = int(j,16)
        #print "next: " +  " " + repr(int(i,16)) + ' ' + repr(int(j,16))
        #raw_input("press")
        stat = canWrite(c_int(hnd1), c_int(can_id), pointer(msg), c_int(2), c_int(0))
        if stat < 0:
            print "canWrite channel 1 failed: ", stat
            assert(0)
        w.write(repr(int(i,16)) + " " + repr(int(j,16)) + '\n')
        time.sleep(.01)

w.flush()
w.close()
print "done"
# Some cleanup, which would be done acutomatically when the DLL unloads.
stat = canBusOff(c_int(hnd1))

canClose(c_int(hnd1))


