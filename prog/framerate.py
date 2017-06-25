#!/usr/bin/python  -u


def framerate(fname) :
	with open(fname, "r") as f:
		[first_frame,first_stamp]=f.readline().split()
		count=1
		for line in f: count += 1
		[last_frame,last_stamp]=line.split()
	return (int(last_stamp)-int(first_stamp))/float(count)/1000


if __name__ == "__main__":
	import argparse

	p = argparse.ArgumentParser(description='Framerate (sec/frame) from timestamps')
	p.add_argument('-i', action='store', dest='inp', metavar='FILE', 
                help='Timestamp FILE', required=True)

	args=p.parse_args()

	print framerate(args.inp)

	

