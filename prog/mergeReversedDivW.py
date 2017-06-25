#!/usr/bin/python  -u
PYTHONUNBUFFERED=1

import os
import sys
import argparse
import numpy as np
from scipy.fftpack import rfft
import cmath

rev = []		# reversed txt

def readFile(type):
	global rev
	if type == "rev" : filename = args.revFname
	else : filename = args.divFname
	try:
		with  open(filename, "r") as f:
			for line in f.readlines():
				l = line.split() 
				l[0] = int(l[0])
				l[1] = int(l[1])
				l[2] = float(l[2])
				if type == "rev" :
					#reverse = [l[0], l[1], l[2]]
					rev.append(l)
				if type == "div":
					l[3] = float(l[3])
					if len(rev) == 0:
						readFile("rev")
					for i, r in enumerate(rev):
						if r[0] == l[0] and r[1] == l[1]:
							# x y div-w weight
							print r[0], r[1], r[2] * l[2], l[3]
	except:
		print "Input file does not exist or is not suitable for fourier calculation."
		sys.exit()


#            MAIN 

p = argparse.ArgumentParser(description='Calculate reversed divergence of a div-w file. )')
p.add_argument('-div', action='store', required = True, dest='divFname', metavar='FILE', 
                help='Input div-w file (4 column: x  y  div   weight).')
p.add_argument('-rev', action='store', required = True, dest='revFname', metavar='FILE',
                help='Input reversed file (3 column: x  y  +-1).The last column stands as a boolean, +1 if is not reversed, -1 if reversed.')
args=p.parse_args()

readFile("rev")
readFile("div")
