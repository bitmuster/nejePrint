
import serial
import time
import sys
import struct
import math

# http://python-pillow.github.io/
from PIL import Image

# install pyserial: https://pyserial.readthedocs.io/en/latest/pyserial.html



# Burn / Engrave
#
# python3 printer_new_protocol.py <burn_time> <filename>
#
# python3 printer_new_protocol.py 9 Openclipart_Cybernetic_Brain_Line_Art_1538347045_eroded_451.png

# Run Tests:
# python3 -m unittest test_printer_new_protocol.py

HELLO = b"\xff\x09\x5a\xa5"
ACK = b'\xff\x05\x01\x01'
DOIT = b'\xff\x06\x01\x01'
WHATEVER = b'\xff\x6e\x01\x02\x28\x02\x28'

DIMENSIONS_T = b'\xff\x6e\x02'

# According to the manual the printer can work on
# >>> 0.075*490 = 36.75 mm
# However the sofware allows a maximum size of 451px
#
# WTF file with max size 451 : data: 04 38 04 33

# further sniffed codes:
# ff 04 01 00 stop
# ff 01 02 00 pause
# ff 01 01 00 start
# ff 02 01 00 cut a border ?

# Another sequence
# ff 6e 01 01 48 00 13
# ff 6e 02 01 2e 04 33
# ff 02 02 00
# then
# ff 02 01 00 cut a border ?

d = 0.1 # slow down to observe

debug = False

def init_serial():
    ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1.0)
    return ser

def init(ser, burn_time):

    print("Read buffer")
    rep=ser.read(30);
    #print(rep)

    print("Say hello to printer")
    ser.write(HELLO)

    rep=ser.read(20);
    #print('Read', len(rep), 'bytes')

    exp_a = b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n\x00'
    exp_b = b'\xff\r\x00d\xff\x10\x01\x00'

    if len(rep) != 20:
        print('Oh')
        print('Device responded with', rep)
        sys.exit(1)

    if rep.startswith(exp_a) and rep.endswith(exp_b):
        pass
    else:
        print('Ooh')
        print('Device responded with', rep)
        sys.exit(1)

    print('Write intensity')
    time.sleep(d)

    # Todo Will not work for times larger than 0xff!
    intensity = b'\xff\x05' + struct.pack('b', burn_time) + b'\x00' #20ms

    ser.write(intensity)

    print('Write \'whatever\'')
    time.sleep(d)
    ser.write(WHATEVER)

def derive_dimensions(width_bytes, height):
    # I don't want to know ho invented that algrrithm
    # Multiples of 100 are in the MSB, the rest ( v-x*msb) in the LSB
    # But not always

    # Interpretation hreshhold unknown somewhere betweeen 0x80 and 180
    th = 0x80

    if width_bytes*8 <= th:
        x = 0
        y = width_bytes*8
        w = struct.pack('BB', x, y)
    else:
        x = (width_bytes*8) // 100
        y = width_bytes*8 -x*100
        w = struct.pack('BB', x, y)

    if height <= th:
        x = 0
        y = height
        h = struct.pack('BB', x, y)
    else:
        x = height // 100
        y = height -x*100
        h = struct.pack('BB', x, y)

    dim = DIMENSIONS_T + w + h

    return dim

def image(ser, filename):

    print('Write dimensions')
    time.sleep(d)

    im = Image.open(filename)
    print('Image size:', im.size)

    # Seems to be the case when we read from png instead of bmp
    invert = True

    #im = im.resize((512,512), Image.NEAREST)
    #im = im.convert('1') #.transpose(Image.FLIP_TOP_BOTTOM)
    #print(im.tobytes())
    u = im.tobytes()

    iw = im.size[0] # intentional width
    ih = im.size[1] # intentional height

    if invert:
        u = u.replace(b'\x00',b'\x02')
        u = u.replace(b'\x01',b'\x00')
        u = u.replace(b'\x02',b'\x01')

    if debug:
        # the binary image:
        for i in range(len(u)):
            print(u[i], end='')
            if ((i+1)% iw) ==0:
                print('')

    #print(im)

    data_width = math.ceil(iw/8)

    print('Data Width', data_width)

    padbits = data_width*8 - iw

    print('Image size:', im.size)
    print('Bits to pad: ', padbits)
    
    print('Data width: ', data_width, 'Bytes')
    print('Data width: ', data_width * 2, 'Hex-Chars')
    print('Will create blob with', data_width*ih , 'Bytes')

    rows=[]
    data = b''
    val = 0

    for i in range(len(u)):
        assert  u[i] == 0 or u[i] == 1
        val = val << 1
        val += u[i]
        if ((i+1)% iw) ==0:
            val = val << padbits;
            
            rows.append(val)

            if debug:
                print(hex(val))

            s=f'{{0:{data_width}x}}'
            data += bytes.fromhex(s.format(val))
            val=0

    print('Data Length is: ', len(data))

    assert len(data) == math.ceil(iw/8)*ih

    dim = derive_dimensions(data_width, ih)

    #print(dim)
    ser.write(dim)

    print('Write DO IT')
    time.sleep(d)
    ser.write(DOIT)

    print("Read and hope for ACK")
    rep=ser.read(10);

    if len(rep) != 4:
        print('Error in response length')
        print('Device responded with', rep)
        sys.exit(1)

    if rep == ACK:
        pass
    else:
        print('Error in response')
        print('Device responded with', rep)
        sys.exit(1)

    print('Write image data')
    time.sleep(d)

    ser.write(data)

    with open(filename + '.img','bw') as f:
        f.write(data)

    # next response ia
    # ff 0b 00 00
    # garbage about the process


def send_stop(ser):
    # works
    STOP = b'\xff\x04\x01\x00'
    ser.write(STOP)

def cut_border(ser):
    # does not work
    wtf1 = b'\vff\v6e\v01\v01\v48\v00\v13'
    wtf2 = b'\vff\v6e\v02\v01\v2e\v04\v33'

    ser.write(wtf1)
    time.sleep(d)
    ser.write(wtf1)
    time.sleep(d)

    BORDER = b'\xff\x02\x01\x00'
    ser.write(BORDER)

if __name__ == '__main__':

    # 50: white paper engrave
    # 20: not so white paper engrave
    # 5-10: engrave light balsa wood
    burn_time = int(sys.argv[1])

    #filename = './test_50x50.bmp'
    filename = sys.argv[2]
    #filename = 'Openclipart_Cybernetic_Brain_Line_Art_1538347045_eroded.png'
    #filename = 'Openclipart_Cybernetic_Brain_Line_Art_1538347045_half.png'
    #filename = 'ryanlerch-skull-and-crossbones_250px_border.png'
    #filename = 'ryanlerch-skull-and-crossbones_125px_border.png'

    ser = init_serial()

    #send_stop(ser)
    #cut_border(ser)

    init(ser, burn_time)
    image(ser, filename)




