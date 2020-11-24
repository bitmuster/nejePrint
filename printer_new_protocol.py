
import serial
import time
import sys
import struct
import math

# http://python-pillow.github.io/
from PIL import Image

# install pyserial: https://pyserial.readthedocs.io/en/latest/pyserial.html

HELLO = b"\xff\x09\x5a\xa5"
ACK = b'\xff\x05\x01\x01'
DOIT = b'\xff\x06\x01\x01'
WHATEVER = b'\xff\x6e\x01\x02\x28\x02\x28'

DIMENSIONS_T = b'\xff\x6e\x02'

d = 0.1 # slow down to observe

def init_serial():
    ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1.0)
    return ser

def init(ser, burn_time):

    print("Read buffer emtty")
    rep=ser.read(30);
    print(rep)

    print("Say hello")
    ser.write(HELLO)

    print("Read 20")
    rep=ser.read(20);
    print('Read ', len(rep), ' bytes')

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

    print('intensity')
    time.sleep(d)

    # Todo Will not work for times larger than 0xff!
    intensity = b'\xff\x05' + struct.pack('b', burn_time) + b'\x00' #20ms

    ser.write(intensity)

    print('Write whatever')
    time.sleep(d)
    ser.write(WHATEVER)


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

    # the binary image:
    for i in range(len(u)):
        print(u[i], end='')
        if ((i+1)% iw) ==0:
            print('')

    print(im)

    #width = b'\x00\x10'  # bit width

    if (iw % 8) ==0:
        w = iw//8
    else:
        w = iw//8+1

    print('Data Width', w)

    padbits = w*8 - iw

    print('Image size:', im.size)
    print('Bits to pad: ', padbits)
    data_width = math.ceil(iw/8)
    assert data_width == w # same value different calculation
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
            print(hex(val))

            s=f'{{0:{data_width}x}}'
            data += bytes.fromhex(s.format(val))
            val=0

    print('Data Length: ', len(data))

    assert len(data) == math.ceil(iw/8)*ih

    width = height = struct.pack('>h', w*8) # should be a multiple of 8

    #height = b'\x00\x0a' # 10 lines
    height = struct.pack('>h', ih)

    dim = DIMENSIONS_T + width + height
    print(dim)
    ser.write(dim)

    print('Write DO IT')
    time.sleep(d)
    ser.write(DOIT)

    print("Read and hope for ACK")
    rep=ser.read(10);

    if len(rep) != 4:
        print('Ah')
        sys.exit(1)

    if rep == ACK:
        pass
    else:
        print('Aah')
        sys.exit(1)

    print('Write data')
    time.sleep(d)

    ser.write(data)

    with open(filename + '.img','bw') as f:
        f.write(data)


if __name__ == '__main__':

    # 50: white paper engrave
    # 20: not so white paper engrave
    # 5-10: engrave light balsa wood
    burn_time = 5

    #filename = './test_50x50.bmp'
    #filename = 'Openclipart_Cybernetic_Brain_Line_Art_1538347045_half.png'
    #filename = 'ryanlerch-skull-and-crossbones_250px_border.png'
    filename = 'ryanlerch-skull-and-crossbones_125px_border.png'

    ser = init_serial()
    init(ser, burn_time)
    image(ser, filename)




