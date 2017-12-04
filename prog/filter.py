#!/usr/bin/python  -u
PYTHONUNBUFFERED=1

import os
import sys
import argparse
import numpy as np
import itertools
import ntpath

import sqlite3

fileNames = []

def getXs():
	cursor.execute('SELECT DISTINCT x from divs');
	return sorted([x[0] for x in cursor.fetchall()  ])

def getYs():
	cursor.execute('SELECT DISTINCT y from divs');
	return sorted([x[0] for x in cursor.fetchall()  ])

def medianFilter():
	for (x, y) in itertools.product(xxs, yys):
		lst = []
		cursor.execute("SELECT div  FROM divs WHERE x=? AND y=?", (x, y))
		actdiv  = [xp[0] for xp in cursor.fetchall()][0]
		lst.append(actdiv)
		cursor.execute("SELECT div  FROM divs WHERE x=? AND y=?", (x-grid, y))
		lst.append([xp[0] for xp in cursor.fetchall()][0])
		cursor.execute("SELECT div  FROM divs WHERE x=? AND y=?", (x+grid, y))
		lst.append([xp[0] for xp in cursor.fetchall()][0])
		cursor.execute("SELECT div  FROM divs WHERE x=? AND y=?", (x, y+grid))
		lst.append([xp[0] for xp in cursor.fetchall()][0])
		cursor.execute("SELECT div  FROM divs WHERE x=? AND y=?", (x, y-grid))
		lst.append([xp[0] for xp in cursor.fetchall()][0])
		newdiv = sorted(lst)[2]
		cursor.execute("SELECT fileId, x, y  FROM divs WHERE x=? AND y=?", (x, y))
		data = cursor.fetchall()
		print data[0][1], data[0][2], newdiv

def highPassFilter(alpha):
	print "High pass filtering in process.."
	for(x,y) in itertools.product(xs,ys):
		cursor.execute("SELECT fileId, div FROM divs WHERE x=? AND y=?", (x, y))
		orig = cursor.fetchall()
		fileId = [ z[0] for z in orig ]
		orig_div = [ z[1] for z in orig ]		
		new_div=[]
		new_div.append(orig_div[0])
		for i in range(1, len(fileId)):
			d= alpha * new_div[i-1] + alpha * (orig_div[i] - orig_div[i-1])	
			new_div.append(d)
		if args.ftype == "highpass2" and len(orig_div) > 100:
			mean1=np.average(orig_div[0:100])
			mean2=np.average(new_div[0:100])
			new_div = [z+mean1-mean2 for z in new_div ]
		for d,id in zip(new_div,fileId): 
			cursor.execute(
				"UPDATE divs SET div=? WHERE fileId=? AND x=? AND y=?", 
				(d, id, x, y))
		db.commit()
	print >> sys.stderr, "High pass filter finished"

def calcStat(type):
	for(x,y) in itertools.product(xs,ys):
		cursor.execute("SELECT fileId, div FROM divs WHERE x=? AND y=?", (x, y))
		orig = cursor.fetchall()
		fileId = [ z[0] for z in orig ]
		div = [ z[1] for z in orig ]
		if type == "std":		
			print x, y, np.std(div)
		elif type == 'avg':
			print x, y, np.average(div)

def searchReverse():
	reverse = "+1"
	for(x,y) in itertools.product(xs,ys):
		cursor.execute("SELECT fileId, div FROM divs WHERE x=? AND y=?", (x, y))
		db = cursor.fetchall()
		fileId = [ z[0] for z in db ]
		r      = [ z[1] for z in db ]
		rMin  = min(r)
		rMax  = max(r)
		rMean = np.mean(r)
		if rMean - rMin < (rMax - rMin) / 2 : reverse = "+1"
		else : reverse = "-1"
		print x, y, reverse

def getFileId(fileName):
	first = fileName.rfind('-') + 1
	last = first + 5
	return int(fileName[first:last])

def readFiles():
	for n, f in enumerate(fileNames):
		with open(f, "r") as fileName:
			fileId = getFileId(f)
			for line in fileName.readlines():
				l = line.split()
				if args.r : 
					dx = float(l[2])
					dy = float(l[3])
					r = np.sqrt( dx*dx + dy*dy )
					# Insert displacement  alues in pivs table
					cursor.execute('''INSERT INTO divs(fileId, x, y, div) VALUES(?,?,?,?)''', ( fileId, int(l[0]), int(l[1]), r ) )
				else:
					# Insert div in divs table
					cursor.execute('''INSERT INTO divs(fileId, x, y, div) VALUES(?,?,?,?)''', ( fileId, int(l[0]), int(l[1]), float(l[2]) ) )
	db.commit()
	print >> sys.stderr, "File reading finished."

def writeData():
	if not os.path.exists(args.dir):
		os.makedirs(args.dir)
	#cursor.execute("SELECT fileId, div FROM divs WHERE x=? AND y=?", (x, y))
	for f in fileNames:
		fileId = int(f[-14 : -9])
		filename = args.dir + '/' + ntpath.basename(f)
		print filename
		f = open(filename, 'w')
		cursor.execute("SELECT x, y, div FROM divs WHERE fileId=%d" % fileId)
		for l in cursor.fetchall():
			#print l[0], l[1], l[2]
			w = str(l[0]) +'\t' + str(l[1]) + '\t' + str(l[2]) + '\n'
			f.write(w)
		f.close()

#            MAIN 

p = argparse.ArgumentParser(description='Filter divergence files for noise eliminating.')
p.add_argument('-t', action='store', dest='ftype', choices=['median', 'highpass', 'highpass2', "stdev", "avg"],
                help='Filter type. \n \"median\" median filter. \n \"highpass\" for high pass filter. \n \"stdev\" in case when standard deviation calculation is needed. The deviation of all x, y combinations  will be written to the standard output. \n \"avg\" for average.' )
p.add_argument('-d', action='store', dest='dir', help='Target directory name (new div files will be saved here). In case if high pass filtering.')
p.add_argument('-r', action='store_true', help='Search for reversed pixels in piv0ref files.')
args=p.parse_args()


# read filenames from standard input
for line in sys.stdin:
	fileNames.append( line.strip() )
# Create a database in RAM
db = sqlite3.connect(':memory:')
cursor = db.cursor()
cursor.execute('''CREATE TABLE divs(id INTEGER PRIMARY KEY, fileId INTEGER, x INTEGER, y INTEGER, div FLOAT)''')
cursor.execute('CREATE INDEX divs_idx ON divs(x,y)')
db.commit()

readFiles()
xs = getXs()
ys = getYs()
grid = xs[1] - xs[0]
minx = min(xs)
maxx = max(xs)
miny = min(ys)
maxy = max(ys)
xxs = xs[1:-1]
yys = ys[1:-1]

if args.r:
	searchReverse()
else:
	if args.ftype == "median":
		medianFilter()
	elif args.ftype == "highpass":
		highPassFilter(0.75)
		writeData()
	elif args.ftype == "highpass2":
		highPassFilter(0.9)
		writeData()
	elif args.ftype == "stdev":
		calcStat("std")
	elif args.ftype == "avg":
		calcStat("avg")

db.close()
