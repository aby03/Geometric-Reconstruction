# For resizing images in selected dir
from PIL import Image
import os, sys

#path = "Database/1_A/train2/"
path = "Database/1_A/test_images/"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        print(path+item)
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(item)
            imResize = im.resize((300,300), Image.ANTIALIAS)
            imResize.save(path + '1_' + f + '.jpg', 'JPEG', quality=90)

resize()
