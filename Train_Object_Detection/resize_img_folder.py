# For resizing images in sub-directories of selected directory
from PIL import Image
import os, sys

path = "Database/1_A/train/"
dirs = os.listdir( path )

def resize():
	for item2 in dirs:
		tmp = os.listdir( path+item2 )
		for item in tmp:
			print(path+item2+'/'+item)
			if os.path.isfile(path+item2+'/'+item):
				im = Image.open(path+item2+'/'+item)
				f, e = os.path.splitext(item)
				imResize = im.resize((300,300), Image.ANTIALIAS)
				imResize.save(path+item2+'/1_' + f + '.jpg', 'JPEG', quality=90)

resize()
