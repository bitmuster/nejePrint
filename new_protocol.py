
import serial
import time
import sys
import struct

# install pyserial: https://pyserial.readthedocs.io/en/latest/pyserial.html

ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1.0)

#ser.write(b"\xF6")

HELLO = b"\xff\x09\x5a\xa5"
ACK = b'\xff\x05\x01\x01'
DOIT = b'\xff\x06\x01\x01'
WHATEVER = b'\xff\x6e\x01\x02\x28\x02\x28'

DIMENSIONS_T = b'\xff\x6e\x02'

d = 0.1 # slow down to observe

print("Read buffer emtty")
rep=ser.read(30);
print(rep)

print("Say hello")
ser.write(HELLO)

print("Read 20")
rep=ser.read(20);
print('Read ', len(rep), ' bytes')
print('Read:   ', rep)

# the 11. bit is the intensity
exp = b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n\x00\x0b\xff\r\x00d\xff\x10\x01\x00'
#print('Expected', exp)
exp2 = b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n\x002\xff\r\x00d\xff\x10\x01\x00'
exp3 = b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n\x00\x10\xff\r\x00d\xff\x10\x01\x00'

if len(rep) != 20:
    print('Oh')
    sys.exit(1)

if rep == exp or rep == exp2 or rep==exp3:
    pass
else:
    print('Ooh')
    sys.exit(1)


# reads
# b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n'
# b'\x00\x0b\xff\r\x00d\xff\x10\x01\x00'
# b'\xff\x05\x01\x01'

# reads
# b'\xff\x01\x00\x00
#   \xff\x02\x0b\x02
#   \xffx00\x0b
#   \xff\r\x00d
#   \xff\x10\x01\x00'
# b'\xff\x05\x01\x01'


#write
#ff 05 0b 00

print('intensity')
time.sleep(d)

#intensity = b'\xff\x05\x0b\x00' #11ms
#intensity = b'\xff\x05\x32\x00' #50ms
#intensity = b'\xff\x05\x14\x00' #20ms
intensity = b'\xff\x05\x10\x00' #16ms
ser.write(intensity)

#write
#ff 6e 01 02 28 02 28 ff 6e 02 00 10 00 0a ff 06 01 01

print('Write whatever')
time.sleep(d)
ser.write(WHATEVER)

print('Write dimensions')
time.sleep(d)

#width = b'\x00\x10'  # bit width
width = height = struct.pack('>h', 16) # should be a multiple of 8

#height = b'\x00\x0a' # 10 lines
height = struct.pack('>h', 10)

dim = DIMENSIONS_T + width + height
ser.write(dim)

print('Write DO IT')
time.sleep(d)
ser.write(DOIT)

print("Read and hope for ACK")
rep=ser.read(10);
print(rep)

#read ack

if len(rep) != 4:
    print('Ah')
    sys.exit(1)

if rep == ACK:
    pass
else:
    print('Aah')
    sys.exit(1)


#write
#ff c0 ff c0 ff c0 ff c0 ff c0 ff c0 ff c0 ff c0 ff c0 ff c0

print('data')
time.sleep(d)
data = b'\xff\xc0\xff\xc0\xff\xc0\xff\xc0\xff\xc0\xff\xc0\xff\xc0\xff\xc0\xff\xc0\xff\xc0'
ser.write(data)


