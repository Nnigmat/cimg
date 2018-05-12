#!/usr/bin/python3
import operator
from PIL import Image
import sys
import os
from collections import defaultdict

try:
    arg = str(sys.argv[1]) 
except:
    print("Sorry bro, you haven't add file")


if arg != '' and not '/home' in arg:
   im = Image.open(os.getcwd() + '/' + arg)
else:
   im = Image.open(arg)

by_color = defaultdict(int)
for pixel in im.getdata():
    by_color[pixel] += 1

res = ''
i = 0
for el in sorted(by_color, key=by_color.get, reverse=True):
    res += '#' + str(hex(el[0])[2:]).upper() + str(hex(el[1])[2:]).upper() + str(hex(el[2])[2:]).upper() + ', '
    i += 1
    if i == 50:
        break

print(res.rstrip(', ')) 
