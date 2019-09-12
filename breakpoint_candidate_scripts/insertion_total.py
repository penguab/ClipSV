#!/usr/bin/env python	
import sys,re
	
def insertion_total(clips_insertion,large_insertion,translocation):
	out_file=open('insertion_total','w')	
	total=[]
	for i in [clips_insertion,large_insertion,translocation]:
		with open(i) as f:
			while True:
				l=f.readline().rstrip()
				if not l: break
				line=l.split('\t')
				if i==clips_insertion:
					total.append([line[0],line[1],str(int(line[1])+1),"INS",line[4],i])
				else:
					total.append([line[0],line[1],str(int(line[1])+1),"INS","-",i])
	total_sorted=sorted(total,key=lambda x: (x[0], int(x[1]),int(x[2])))
	for x in range(len(total_sorted)):
		out_file.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')
	
