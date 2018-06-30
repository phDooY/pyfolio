# uncompyle6 version 3.2.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Dec  4 2017, 14:50:18) 
# [GCC 5.4.0 20160609]
# Embedded file name: /root/pyfolio/text2png.py
# Compiled at: 2018-01-10 19:30:47
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def text2png(text, fullpath, color='#000', bgcolor='#FFF', fontfullpath=None, fontsize=15, leftpadding=3, rightpadding=3):
    font = ImageFont.load_default() if fontfullpath == None else ImageFont.truetype(fontfullpath, fontsize)
    lines = text.splitlines()
    max_width = 0
    longest_line = ''
    for i in lines:
        if len(i) > max_width:
            longest_line = i
            max_width = len(i)

    width = font.getsize(longest_line)[0] + rightpadding + leftpadding
    line_height = font.getsize(text)[1]
    img_height = line_height * (len(lines) + 1)
    img = Image.new('RGBA', (width, img_height), bgcolor)
    draw = ImageDraw.Draw(img)
    y = 0
    for line in lines:
        draw.text((leftpadding, y), line, color, font=font)
        y += line_height

    img.save(fullpath)
    return
