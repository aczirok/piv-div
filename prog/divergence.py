#!/usr/bin/python  -u
PYTHONUNBUFFERED=1

import os
import sys
import argparse
import numpy as np

poi = {}		# values from piv0 file: key(x	y) : value(dx	dy)
cx = set([])		# store all possible x coordinate (sorted)
cy = set([])		# store all possible y coordinate (sorted)

def readPiv():
	global cx, cy, poi
	try:
		with  open(args.piv, "r") as f:
			for line in f.readlines():
				l = line.split()
				l[0]=int(l[0])
				l[1]=int(l[1])		
				poi[(l[0], l[1])] = (float(l[2]), float(l[3]))	
				cx.add(l[0])
				cy.add(l[1])
		cx=sorted(list(cx))
		cy=sorted(list(cy))
	except:
		print "Input file does not exist or is not suitable for divergence calculation."
		sys.exit()

def getGridConstant():
	return cx[1] - cx[0]

def getNeighbors(pointX, pointY, grid):
	try:
		right = poi[(pointX + grid, pointY)]
		left  = poi[(pointX - grid, pointY)]
		upper = poi[(pointX, pointY + grid)]
		lower = poi[(pointX, pointY - grid)]
		return [right[0], left[0], upper[1], lower[1]]
	except: pass
	 
def calcDiv(n, grid):
	dxvx = (n[0] - n[1]) / 2 * grid
	dyvy = (n[2] - n[3]) / 2 * grid
	return dxvx + dyvy

def process():
	grid = getGridConstant()
	for i in cx[1:-1]:
	    for j in cy[1:-1]:
		k=(i,j)
		neighs = getNeighbors(k[0], k[1], grid)
		if neighs == None: 
			print k[0], k[1], "NaN"
			continue
		div = calcDiv(neighs, grid)
		print k[0], k[1], div

#            MAIN 

p = argparse.ArgumentParser(description='Calculate divergence of a piv0 file.')
p.add_argument('-i', action='store', dest='piv', metavar='FILE', 
                help='Input piv0 file')
args=p.parse_args()

readPiv()
process()
