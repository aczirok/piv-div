#!/usr/bin/python  -u
PYTHONUNBUFFERED=1

import os 
import sys 
import argparse
import numpy as np
from collections import namedtuple

div = dict()
pivw = dict()
keys = []

def readInput(fileName, dictionary, typeOfFile) :
	with  open(fileName, "r") as f:
		for line in f.readlines():
			l = line.split()
			key = (int(l[0]), int(l[1]))
			if typeOfFile == div: 
				value = (float(l[2]), 0)	# value is a 2d tuple (divergence, weight=0) for now
				keys.append(key)
			else: 
				value = float(l[4])
			dictionary[key] = value

def addweights():
	global div
	for (key1,key2) in div:
		# sometimes pivw does not contain the given pixel
		try:
			key=(key1, key2)
			weight = pivw[key]		# pivw weight
			orig_div = div[key][0]		# because div value is a 2d tuple (divergence, weight). Weight now is 0, this should be replaced with the values from the pivw files.
		except KeyError, e:
			#print 'I got a KeyError - reason "%s"' % str(e)
			continue
		except IndexError, e:
			#print 'I got an IndexError - reason "%s"' % str(e)
			continue
		divvalue = (orig_div, weight)
		div[key] = divvalue

def writeWeightedDiv():
	with open(args.outFile, 'w') as f:
		for (key1, key2) in keys:
			key = (key1, key2)
			try: value = div[key]
			except : continue
			output = str(key[0]) + " " + str(key[1]) + " " + str(value[0]) + " " + str(value[1]) + "\n"
			f.write(output)	
	f.close()

#            MAIN 

p = argparse.ArgumentParser(description='Add weight to divergence file.')
p.add_argument('-d', action='store', dest='divFile', metavar='FILE', 
                help='Input divergence (div) file.')
p.add_argument('-p', action='store', dest='pivwFile', metavar='FILE', 
                help='Input weighted piv0 file.')
p.add_argument('-o', action='store', dest='outFile', metavar='FILE',
		help='Output weighted divergence file.')

args=p.parse_args()

readInput(args.divFile, dictionary = div, typeOfFile=div)
readInput(args.pivwFile, dictionary = pivw, typeOfFile=pivw)
addweights()
writeWeightedDiv()
