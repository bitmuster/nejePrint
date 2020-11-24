


import unittest
import math
from unittest.mock import patch, MagicMock, call

import printer_new_protocol

class TestNewProtocol(unittest.TestCase):

    @patch('printer_new_protocol.serial')
    def test_init_serial(self, mock):
        ret = printer_new_protocol.init_serial()
        mock.Serial.assert_called_once_with('/dev/ttyUSB0', 57600, timeout=1.0)

    def test_init(self):
        expect1 = b''
        expect2 = b'\xff\x01\x00\x00\xff\x02\x0b\x02\xff\n\x00\x0b\xff\r\x00d\xff\x10\x01\x00'
        mock= MagicMock()
        calls = [
            call(printer_new_protocol.HELLO),
            call(b'\xff\x05\x05\x00'),
            call(printer_new_protocol.WHATEVER),
            ]
        mock.read.side_effect = [ expect1, expect2, expect1]
        burn = 5
        printer_new_protocol.init(mock, burn)
        mock.write.assert_has_calls(calls)

    def test_image_skull(self):
        expect1 = printer_new_protocol.ACK
        mock= MagicMock()
        filename = 'ryanlerch-skull-and-crossbones_125px_border.png'
        filename_expect = 'ryanlerch-skull-and-crossbones_125px_border.png.img'
        with open(filename_expect, 'br') as f:
            skull = f.read()

        calls = [
            call(b'\xffn\x02\x00\x80\x00}'), # Image dimensions :128, 125
            call(printer_new_protocol.DOIT),
            call(skull)
            ]
        mock.read.side_effect = [ expect1 ]

        printer_new_protocol.image(mock, filename)

        mock.write.assert_has_calls(calls)

    def test_hex_conversion(self):

        a = 0xc0000781f00003fffe00007c0f000018
        ar = f'{a:032x}'
        ae = 'c0000781f00003fffe00007c0f000018'
        self.assertEqual(ar, ae)

        w = 32
        s=f'{{0:{w}x}}'
        ar2 = s.format(a)
        self.assertEqual(ar2, ae)



    def test_derive_dimensions(self):

        width = 7 # 50px -> 56 bit -> 7 byte
        height = 50
        exp = b'\xff\x6e\x02' # 0x6e = 'n'
        dim = printer_new_protocol.derive_dimensions(width, height)
        self.assertEqual(dim, exp + b'\x00\x38\x00\x32')

        table = [
            [256, b'\x02\x38\x02\x38'],  # 0x38 = '8'
            [255, b'\x02\x38\x02\x37'],
            [200, b'\x02\x00\x02\x00'],
            [180, b'\x01\x54\x01\x50'], # 0x0154 : 100 + 0x54 = 100+ 84= 184
            [451, b'\x04\x38\x04\x33'],
            [125, b'\x00\x80\x00\x7d'],
            ]

        for entry in table:
            w = math.ceil( entry[0] / 8)
            h = entry[0]
            dim = printer_new_protocol.derive_dimensions(w, h)
            self.assertEqual(dim, exp + entry[1])



