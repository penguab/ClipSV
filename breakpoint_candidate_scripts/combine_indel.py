#!/usr/bin/env python	
import sys,re
	
def combine_indel(clips_filter_indel,overlapping_filter_indel,indel_filter,duplication_INDEL,out_name):
	out_file=open(out_name,'w')	
	total=[]
	info={}
	for i in [clips_filter_indel,overlapping_filter_indel,indel_filter,duplication_INDEL]:
		with open(i) as f:
			while True:
				l=f.readline().rstrip()
				if not l: break
				line=l.split('\t')
				name='\t'.join(line)
				if not name in info:
					total.append(line)
				info[name]=1
	total_sorted=sorted(total,key=lambda x: (x[0], int(x[1]),int(x[2])))
	for x in range(len(total_sorted)):
		out_file.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')
