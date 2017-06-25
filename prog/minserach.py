#!/usr/bin/python  -u
PYTHONUNBUFFERED=1

import os
import sys
import argparse
#import maxsearch
import numpy as np

""""
Calculate min for reference piv0.
"""

def calcMin() :
	data = []
	with open(args.input, "r") as f:
		for line in f.readlines():
			w = line.split()
			data.append([w[0], float(w[1])])
	mindispl = 10000				# minimum displacement
	minframe = 0
	for i in range(len(data)):
		if data[i][1] < mindispl :
			mindispl = data[i][1]
			minframe = data[i][0]
	print minframe

#            MAIN

p = argparse.ArgumentParser(description='Calculate min for piv0 reference.')
p.add_argument('-i', action='store', dest='input', metavar='FILE',
                help='Input txt file')

args=p.parse_args()

calcMin()

