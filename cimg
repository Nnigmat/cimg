#!/usr/bin/python3
import operator
from PIL import Image
import sys
import os
from collections import defaultdict

home = '/home/nigma/'

try:
    arg = str(sys.argv[1]) 
except:
    print("Sorry bro, you haven't add file")
    sys.exit()

exten = None
try:
    exten = arg.split('.')[1]
except:
    pass

if arg != '' and not '/home' in arg:
   im = Image.open(os.getcwd() + '/' + arg)
elif arg != '' and '~/' in arg:
   im = Image.open(home + arg)
else:
   im = Image.open(arg)

if not exten or exten.lower() != 'gif':
    by_color = defaultdict(int)
    for pixel in im.getdata():
        print(pixel)
        by_color[pixel] += 1
else:
    rgbim = im.convert('RGB')
    print(dir(rgbim))
    print(rgbim.getpixel((0,0)))
    print(rgbim.size)
    
    by_color = defaultdict(int)
    for pixel in rgbim.getdata():
        by_color[pixel] += 1

res = ''
i = 0
print(sorted(by_color, key=by_color.get, reverse=True))
for el in sorted(by_color, key=by_color.get, reverse=True):
    res += '#' + str(hex(el[0]))[2:].upper() + str(hex(el[1]))[2:].upper() + str(hex(el[2]))[2:].upper() + ', '
    i += 1
    if i == 50:
        break

print(res.rstrip(', ')) 
