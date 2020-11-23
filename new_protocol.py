
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
#print('Read:   ', rep)

# the 11th bit is the intensity
exp = b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n\x00\x0b\xff\r\x00d\xff\x10\x01\x00'
#print('Expected', exp)
exp2 = b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n\x002\xff\r\x00d\xff\x10\x01\x00'
exp3 = b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n\x00\x10\xff\r\x00d\xff\x10\x01\x00'

exp_a = b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n\x00'
exp_b = b'\xff\r\x00d\xff\x10\x01\x00'

if len(rep) != 20:
    print('Oh')
    sys.exit(1)

if rep.startswith(exp_a) and rep.endswith(exp_b):
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
#intensity = b'\xff\x05\x10\x00' #16ms

# 50: white paper engrave
# 20: not so white paper engrave

burn_time = 20
intensity = b'\xff\x05' + struct.pack('b', burn_time) + b'\x00' #20ms

ser.write(intensity)

#write
#ff 6e 01 02 28 02 28 ff 6e 02 00 10 00 0a ff 06 01 01

print('Write whatever')
time.sleep(d)
ser.write(WHATEVER)


def rectangle_10x10():

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
    #print(rep)

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

skull= "00 00 00 00 ff ff c0 00 00 00 00 00 00 00 0f f0 " + \
"03 fc 00 00 00 00 00 00 00 7c 00 00 1f 80 00 00 " + \
"00 00 00 01 e0 00 00 01 e0 00 00 00 00 00 03 80 " + \
"00 00 00 70 00 00 00 00 00 06 00 00 00 00 18 00 " + \
"00 00 00 00 0c 00 00 00 00 0c 00 00 00 00 00 18 " + \
"00 00 00 00 06 00 00 00 00 00 30 00 00 00 00 03 " + \
"00 00 00 00 00 60 00 00 00 00 01 80 00 00 00 00 " + \
"60 00 00 00 00 01 80 00 00 00 00 c0 00 00 00 00 " + \
"00 c0 00 00 00 00 80 00 00 00 00 00 40 00 00 00 " + \
"01 80 00 00 00 00 00 60 00 00 00 01 80 00 00 00 " + \
"00 00 60 00 00 00 01 00 00 00 00 00 00 20 00 00 " + \
"00 03 00 00 00 00 00 00 30 00 00 00 03 18 00 00 " + \
"00 00 02 30 00 00 00 03 18 00 00 00 00 02 30 00 " + \
"00 00 03 10 00 00 00 00 03 30 00 00 00 03 10 00 " + \
"00 00 00 03 30 00 00 00 03 10 00 00 00 00 02 10 " + \
"00 00 00 03 10 00 00 00 00 02 30 00 00 00 03 18 " + \
"00 00 00 00 02 30 00 00 00 03 18 00 00 00 00 06 " + \
"30 00 00 00 01 08 00 00 00 00 06 30 00 00 00 01 " + \
"0c 00 00 00 00 0c 30 00 00 00 01 8c 00 00 00 00 " + \
"0c 60 00 00 00 01 8c 00 00 00 00 0c 60 00 00 00 " + \
"00 cc 03 f0 03 f0 0c 40 00 00 00 00 cc 3f f8 07 " + \
"ff 0c c0 00 00 00 00 6c 7f f8 07 ff 8d 80 00 00 " + \
"00 00 6c ff f8 07 ff cf 80 00 00 00 00 3c ff f8 " + \
"07 ff c7 00 00 00 00 00 1c ff f8 07 ff c6 00 00 " + \
"00 00 00 18 ff f0 03 ff c6 00 00 00 03 00 08 7f " + \
"f0 03 ff 86 00 30 00 07 80 18 7f e0 01 ff 86 00 " + \
"f8 00 0c c0 18 3f c0 00 ff 06 01 cc 00 0c 60 18 " + \
"1f 80 00 7f 02 01 8c 00 08 30 18 0f 01 20 3c 06 " + \
"03 0c 00 08 30 18 00 03 30 00 06 03 04 00 08 18 " + \
"18 00 07 38 00 06 06 04 00 18 0e 08 00 07 38 00 " + \
"04 1c 06 00 30 07 8c 00 07 38 00 0c 78 03 00 60 " + \
"01 e6 00 0f 3c 00 19 e0 01 80 c0 00 7f 80 0f 3c " + \
"00 7f 80 00 c0 c0 00 1f f0 0f 3c 03 fe 00 00 c0 " + \
"e1 c0 07 fc 07 3c 0f f8 00 e1 c0 7f f0 01 de 06 " + \
"18 1e e0 03 ff 80 00 3c 00 57 00 00 1a c0 0f 00 " + \
"00 00 07 80 6b 00 00 35 80 38 00 00 00 01 e0 69 " + \
"00 00 25 81 e0 00 00 00 00 78 29 80 00 25 87 80 " + \
"00 00 00 00 1e 20 c0 00 e1 1e 00 00 00 00 00 07 " + \
"a4 0b f4 29 78 00 00 00 00 00 01 e4 0a 14 29 e0 " + \
"00 00 00 00 00 00 64 0a 14 29 80 00 00 00 00 00 " + \
"00 24 6a 15 81 80 00 00 00 00 00 00 60 0f fc 01 " + \
"80 00 00 00 00 00 01 e3 0a 14 31 e0 00 00 00 00 " + \
"00 07 a1 8a 14 61 78 00 00 00 00 00 1e 30 6a 15 " + \
"83 1e 00 00 00 00 00 78 30 0f fc 03 07 80 00 00 " + \
"00 e1 e0 10 00 00 02 01 e1 c0 00 03 ff 80 18 00 " + \
"00 06 00 3f f0 00 06 08 00 7c 00 00 0f 80 00 18 " + \
"00 06 00 00 e6 00 00 19 e0 00 18 00 06 00 03 87 " + \
"00 00 38 70 00 18 00 03 80 0e 01 c0 00 e0 1c 00 " + \
"30 00 01 c0 3c 00 fc 0f c0 07 00 60 00 00 c0 f0 " + \
"00 1f fe 00 01 c0 c0 00 00 60 c0 00 00 00 00 00 " + \
"c0 80 00 00 61 80 00 00 00 00 00 60 80 00 00 61 " + \
"80 00 00 00 00 00 21 80 00 00 63 00 00 00 00 00 " + \
"00 31 80 00 00 66 00 00 00 00 00 00 19 80 00 00 " + \
"3c 00 00 00 00 00 00 0f 00 00"


def mini_skull():

    print('Write dimensions')
    time.sleep(d)

    #width = b'\x00\x10'  # bit width
    width = height = struct.pack('>h', 8*11) # should be a multiple of 8

    #height = b'\x00\x0a' # 10 lines
    height = struct.pack('>h', 78)

    dim = DIMENSIONS_T + width + height
    ser.write(dim)

    print('Write DO IT')
    time.sleep(d)
    ser.write(DOIT)

    print("Read and hope for ACK")
    rep=ser.read(10);
    #print(rep)

    #read ack

    if len(rep) != 4:
        print('Ah')
        sys.exit(1)

    if rep == ACK:
        pass
    else:
        print('Aah')
        sys.exit(1)

    print('data')
    time.sleep(d)
    data = bytes.fromhex(skull)
    ser.write(data)


#rectangle_10x10()
mini_skull()




