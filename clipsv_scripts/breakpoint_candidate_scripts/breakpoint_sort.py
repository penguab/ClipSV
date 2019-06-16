#!/usr/bin/env python	
import sys,re
	
def breakpoint_sort(breakpoint):
	out=open(breakpoint+'.sort','w')	
	total=[]
	with open(breakpoint) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			line=l.split('\t')
			content=line[-8].split(":")
			if content[0] != "-" and (float(content[0])<0.8 or float(content[1])<0.8):
				continue
			if int(line[9])<20:
				continue
			total.append(line)
	total_sort=sorted(total,key=lambda x: (x[0], int(x[1])))
	for y in range(len(total_sort)):
		out.write(("\t".join(str(n) for n in total_sort[y]))+"\n")

if __name__=="__main__":
	breakpoint=sys.argv[1]
	breakpoint_sort(breakpoint)

