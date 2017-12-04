#!/usr/bin/python  -u
PYTHONUNBUFFERED=1

import os 
import sys 
import argparse
import numpy as np
	

n = []

def calcSum(x, y) :
	return np.sqrt(x**2 + y**2)

def isFloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

def lineAnalysis(line) :
	w = line.split()
	if (w[2] == "NaN" or w[3] == "NaN" or not isFloat(w[2]) or not isFloat(w[3])):
		return
	if args.maskFile is not None:
		if getpix.getpix(int(w[0]),int(w[1]),args.maskFile) < 1 : return
	if args.xy:
		s = args.xy
		if len(s) < 2 : return
		x = int(s[0])
		y = int(s[1])
		if (x-int(w[0]))**2 + (y-int(w[1]))**2 > args.r**2 : return
	n.append(calcSum(float(w[2]), float(w[3])))

def process(fileName) :
	try:
		with  open(fileName, "r") as f:
			for line in f.readlines():
				lineAnalysis(line)
	except IOError:
			print "Could not read file: ", fileName


#            MAIN 

p = argparse.ArgumentParser(description='Usage: Cardiomyocytes Image Processing. Calculates average displacement of piv0 files. Usual ouptut: frame_vs_mean*txt')
p.add_argument('-i', action='store', dest='povFile', metavar='FILE', 
		help='Log FILE')
p.add_argument('-m', action='store', dest='maskFile', metavar='FILE',
		help='A case for area calculation. Optional. Mask: white is ON, black is OFF')
p.add_argument('-xy', action='store', dest='xy', nargs='+',
        help='B case for area calculation. Optional. This parameter must contain X and Y coordianates. X and Y coordinate of a beating center, visually read from average divergence pngs.')
p.add_argument('-x', action='store', dest='x', type=int,
		help='B case for area calculation. Optional. If this parameter is given, Y must also be given. X coordinate of a beating center, visually read from average divergence pngs.')
p.add_argument('-y', action='store', dest='y', type=int,
		help='B case for area calculation. Optional. Y coordinate of a beating center, visually read from average divergence pngs.')
p.add_argument('-r', action='store', dest='r', type=int, default=100,
		help='B case for area calculation. Optional:  radius of the area calculated based on x and y coordinate of the beating center. If no value is given, default = 100.')


args=p.parse_args()

if args.maskFile is not None or (args.x and args.y):
	import getpix

process(args.povFile)
if len(n)>0 : print np.mean(n), np.std(n)
else : print "nan nan"
