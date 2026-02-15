# Very experimental text generator

# http://python-pillow.github.io/
# https://pillow.readthedocs.io/en/stable/reference/ImageFont.html
from PIL import Image
from PIL import ImageFont, ImageDraw

# TODO theese files are not indexed yet

def gen_utf8():

    font = "/usr/share/fonts/truetype/ttf-bitstream-vera/VeraMoBd.ttf"
    image = Image.new("1", [100, 100], color="white")
    draw = ImageDraw.Draw(image)
    # use a truetype font
    size = 100
    size = 40
    font = ImageFont.truetype(font, size)
    string = "Esc\nF1"  # "😱"
    draw.text((0, 0), string, font=font)
    image.save("out.png")


gen_utf8()
