#!/usr/bin/python  -u
PYTHONUNBUFFERED=1

import os
import sys
import argparse
import numpy as np
import glob

frame, value = 0, 0.0
maxFrame, maxValue = -1000000, -1000000.0
minFrame, minValue =  1000000,  1000000.0
maxList = []
minList = []
refList = []
points  = []
frameLimit = 500		# calculations limited only to the first 500 frames

lookForMax = True
digits = None

# After having the positions of the min values from the txt file, created by sum.py, calculate the distance of all minimums from the actual point from the piv0 files
# One piv0 file consists of (x, y, dx, dy) elements

def estimate(d1, d2) :
	l = []
	for k in d1:
		if k not in d2: continue
		dx1, dy1 = d1[k]
		dx2, dy2 = d2[k]
		l.append(np.sqrt((dx1 - dx2)**2 + (dy1 - dy2)**2))
	return np.mean(l)

def getDigits(frame):
	for i in range(2,9):
		try:
			filename = glob.glob(args.piv0 + "/*[_-]" + str(frame).zfill(i) + ".piv0")[0]
			return i
		except:
			continue

def getpiv(frame) :
	global digits
	d = {}
	if digits == None : digits = getDigits(frame)
	try:
		filename = glob.glob(args.piv0 + "/*[_-]" + str(frame).zfill(digits) + ".piv0")[0]
	except:
		return d
	try:
		with open(filename, "r") as f :
			for line in f.readlines():
				x, y, dx, dy = line.split()
				if dx == "NaN" or dy == "NaN": continue
				d[(x,y)] = (float(dx), float(dy))
	except :
		pass
	return d
			

def loopThroughFrames():
	for frame, val in points:
		l = []
		piv = getpiv(frame)
		for minframe, minvalue in refList:
			pivmin = getpiv(minframe) 
			if piv == {} or pivmin == {} : continue
			l.append(estimate(piv, pivmin))
		if len(l) > 1:
			print frame, min(l), np.mean(l)

def search(delta) :
	global maxValue, maxFrame
	global minValue, minFrame
	global lookForMax
	global minList, maxList

	del maxList[:]
	del minList[:]
	for fr, val in points:		# frame and values in points
		if val >  maxValue :
			maxFrame = fr
			maxValue = val
		if val < minValue :
			minFrame = fr
			minValue = val
		if lookForMax :
			if val < maxValue - delta :
				maxList.append((maxFrame,maxValue))
				minValue = val
				minFrame = fr
				lookForMax = False
		else :
			if val > minValue + delta :
				minList.append((minFrame,minValue))
				maxValue = val
				maxFrame = fr
				lookForMax = True

def searchMins() :
#	delta = 0.1
	delta = max([ val for fr,val in points ]) * 0.05			# 5% of the beat pattern max
	while len( minList ) < 5 or len( maxList ) < 5 :
#		print "delta:", delta
		search( delta )  
		delta /= 2
#		print "min:", minList
#		print "max:", maxList


def setPairs(line) :
	global frame, value
	l = line.split()
	frame = int(l[0])
	value = float(l[1])
	if frame > frameLimit : return		# calculations limited only to the first n frames
	points.append((frame, value))

def read() :
	with  open(args.input, "r") as f:
		for line in f.readlines():
			setPairs(line)


def isInverted():
	values = []
	for frame, val in points :
		if frame > 100 : break
		values.append(val)
	mean = np.mean( values )
	min  = np.percentile(  values, 5 )
	max  = np.percentile(  values, 95 )
#	print mean, min, max
	if mean > (max + min) * 0.5 :
		return True
	return  False

def process():
	global refList
	read()
	if isInverted(): 
		refList = maxList
	else : 
		refList = minList
	searchMins()
	loopThroughFrames()
#            MAIN 

p = argparse.ArgumentParser(description = 'Baseline correction. - Calculate the distance of all minimums of piv0 files from minimum values of frame_vs_mean*.txt-s. One piv0 file consists of (x, y, dx, dy) elements. First loop through frame_vs_mean*.txt, than through all  piv0 files found in the given folder.')
p.add_argument('-i', action='store', dest='input', metavar='FILE', 
                help='Input frame_vs_mean*txt file, containing the average displacement of frames (steps).')
p.add_argument('-p', action = 'store', dest = 'piv0', metavar = 'FILE', help = 'Piv0 file folder. The program will list all piv0 files from the folder and will read all piv0 files.')

args=p.parse_args()

process()

