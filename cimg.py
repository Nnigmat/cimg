#!/usr/bin/python3
import operator
from PIL import Image, ImageFilter
import sys
import os
from collections import defaultdict

# Variables declaration
home = '/home/nigma/'
path = None
nOfColors = 20 

# Try to read path to image or its name
try:
    path = str(sys.argv[1]) 
except:
    print("Sorry bro, you haven't add file")
    sys.exit()

# Try to read how many colors we need to return to the user
try:
    nOfColors = int(sys.argv[2])
except:
    pass    

# Open image
# If user pass to us path with /home... or ~/ we need to find this file into filesystem 
# Otherwise this image contains in current directory, or not :)
im = None
if path and path != '' and (not '/home' in path or not '~/' in path):
   im = Image.open(os.getcwd() + '/' + path)
elif path and path != '' and '~/' in path:
   im = Image.open(home + path)
elif path and path != '':
   im = Image.open(path)
else:
   print('Sorry but path to image or its name is invalid')
   sys.exit()


# Convert opened image to RGB format
# We do this, because for example Gif images stores in another format
im = im.filter(ImageFilter.GaussianBlur(10))
im = im.convert('RGB').convert('P', palette = Image.ADAPTIVE, colors=nOfColors).convert('RGB', palette = Image.ADAPTIVE)

# Count all pixels in image
by_color = defaultdict(int)
for pixel in im.getdata():
    by_color[pixel] += 1


# Sort all elements in dictionary of pixels and return n the most used
res = ''
i = 0
for el in sorted(by_color, key=by_color.get, reverse=True):
    color = '' + str(hex(el[0]))[2:].upper() + str(hex(el[1]))[2:].upper() + str(hex(el[2]))[2:].upper() 
    res += '\x1b[48;2;' + str(el[0]) + ';' + str(el[1]) + ';' + str(el[2]) + 'm' + color + '\x1b[0m'
    i += 1
    if i == nOfColors: 
        break

print(res) 
