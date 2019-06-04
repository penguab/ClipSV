#!/usr/bin/env python	
import sys,re
	
def large_insertion_sort(large_insertion):
	out_file=open(large_insertion+'.sort','w')	
	total=[]
	with open(large_insertion) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			line=l.split('\t')
			if line[4].split(":")[1]=="NA":
				continue
			if int(line[9])<60:
				continue
			base=line[16].split(':')
			if float(base[0])<0.3 or float(base[1])<0.3:
				continue
			line[2]=str(int(line[1])+1)
			total.append(line)
	total_sorted=sorted(total,key=lambda x: (x[0], int(x[1])))
	for x in range(len(total_sorted)):
		out_file.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')
	
if __name__ =="__main__":
	large_insertion_sort(sys.argv[1])
