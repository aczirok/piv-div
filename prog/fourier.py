#!/usr/bin/python  -u
PYTHONUNBUFFERED=1

import os
import sys
import argparse
import numpy as np
from scipy.fftpack import rfft
import cmath

data  = []
frame = []

def readFile():
	try:
		with  open(args.filename, "r") as f:
			for line in f.readlines():
				l = line.split()
				frame.append( float(l[0]) )
				data.append( float(l[1]) )
	except:
		print "Input file does not exist or is not suitable for fourier calculation."
		sys.exit()

def calcFourier():
	ps = np.abs( np.fft.rfft(data) )**2 
	avg = np.mean(ps[3:])*len(ps[3:])
	T = frame[-1] - frame[0]
	for i, p in enumerate(ps):
		if i < 3 : continue
		print i/float(T), p / avg, p

#            MAIN 

p = argparse.ArgumentParser(description='Calculate fourier of a two column file. Assuming the first column`s data in continuous, we only calculate with the second data column. Output: frequency (1/T, 2/T, 3/T,...), p/avg, p')
p.add_argument('-i', action='store', dest='filename', metavar='FILE', 
                help='Input two column file')
args=p.parse_args()

readFile()
calcFourier()
