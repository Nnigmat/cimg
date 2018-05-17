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
console = False

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

# Try to read where we need to print result, to console or further to the window application
console = True if '-c' in sys.argv else False

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
im = im.convert('RGBA')
im = im.filter(ImageFilter.GaussianBlur(10))
im = im.convert('P', palette = Image.ADAPTIVE, colors=nOfColors).convert('RGB', palette = Image.ADAPTIVE)

# Count all pixels in image
by_color = defaultdict(int)
for pixel in im.getdata():
    by_color[pixel] += 1


res_array = sorted(by_color, key=by_color.get, reverse=True)
res_array.sort(key=sum, reverse=True)
nOfColors = len(res_array) if len(res_array) < nOfColors else nOfColors
if __name__ == '__main__' and console: 
    # Sort all elements in dictionary of pixels and return n the most used
    res = ''
    color_res = ''
    i = 0
    for el in res_array:
        color = '' + str(hex(el[0]))[2:].upper() + str(hex(el[1]))[2:].upper() + str(hex(el[2]))[2:].upper() 
        color_res += '#' + color + ', ' 
        res += '\x1b[48;2;' + str(el[0]) + ';' + str(el[1]) + ';' + str(el[2]) + 'm                  \x1b[0m  #' + color + '\n'
        i += 1
        if i >= nOfColors: 
            break

    res += color_res.strip(', ')
    print(res) 
else:
    from main import drawColors 
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = drawColors(res_array, nOfColors)
    sys.exit(app.exec_())
