


import unittest
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
        printer_new_protocol.init(mock)
        mock.write.assert_has_calls(calls)

