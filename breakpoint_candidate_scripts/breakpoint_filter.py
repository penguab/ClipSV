#!/usr/bin/env python	
import sys,re
	
def breakpoint_filter(breakpoint):
	out=open(breakpoint+'.filter','w')	
	total=[]
	with open(breakpoint) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			line=l.split('\t')
			if int(line[6])>=3:
				total.append(line)
	total_sort=sorted(total,key=lambda x: (x[5],x[0], int(x[1]),int(x[3])))
	for y in range(len(total_sort)):
		out.write(("\t".join(str(n) for n in total_sort[y]))+"\n")

