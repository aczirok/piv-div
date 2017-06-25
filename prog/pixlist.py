#!/usr/bin/python

from PIL import Image
import sys

if len(sys.argv) < 2:
	sys.stderr.write("pixlist img < list_of_pixels\n")
	sys.exit(1)

img=Image.open(sys.argv[1])
pix = img.load()
for line in sys.stdin:
	w = line.split()
	print line.strip(), pix[int(float(w[0])),int(float(w[1]))]
