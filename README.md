

# Project Restart for Device DK-8-KZ

It seems like the Neje DK-8-KZ speaks a different protocoll than in the
original project. Here we add some magic to be able to use it with scripts
again.

Why? The original software was so cr*** that it was easier to rewrite it than
using it. The device seems to use a simple, though cursed protocol on a usb⁻tty.

Overall, I would not recommend to by this device. The hardware is maximal
cheap and barely functional, the original software is also barely working.
From the price perspective this was probably the expectation though. I did
not by it and it basically appeared for me and was free to use, so I made it
useable.

Changelog

* Add exemplary script to drive a printer with the new/different protocol of
     the DK-8-KZ [11.2020]
* Still a bad hack but started to print images [11.2020]
* Maintenance [01.2026]

Burn / Engrave:

    python3 printer_new_protocol.py <burn_time> <filename>
    python3 printer_new_protocol.py 10 logo_bw_bold.png
    python3 printer_new_protocol.py 9 Openclipart_Cybernetic_Brain_Line_Art_1538347045_eroded_451.png

The burn_time is given in ms and is material specific. Here are some of my
experiences:

* 1 ms  : Test run
* 50 ms : White ABS plastic

Initialise environment (will differ depending on your OS)

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

Testrun (with minimum power)

    python3 printer_new_protocol.py 1 tests/hello.png 



# Original Project Discontinued

2017-06-11 **__Project discontinued due to machine aviability__ Feel free to fork and edit**

Since I didn't figure out how to make Neje Software work on wine.

commands.txt is kind of a retro-engineering log.
It seems to just save a bitmap somewhere and then prints it.

# nejePrint
Linux script for Neje Laser engraver

Usage:
nejePrint.sh SERIALDEVICE IMAGE [BURNINGTIME]

Image must be 520x520 BMP 1 bit color depth (See mono.bmp)



# python3 Neje Printer
Python 3 based Neje Printer script.

If the printer is running just pause before running the script.

Does:
* Image Conversion (Not square images will be stretched)
* Image Load
* Burning Time Setup (With working printer if software already loaded)
* Preview and print (If you really cannot press the button)
* Go home, Reset, Pause

Does not:
* Converted image Preview
* Printed trace view
* Manual Control



Requires:
* Python3
* Pyserial
* Python EasyGUI


More detailed instructions:
http://axengineering.wordpress.com/2016/06/14/neje-laser-engraver-on-linux/
