#!/usr/bin/env python	
import sys,re
	
def combine_SV(clips_filter_SV,overlapping_filter_SV,indel_filter_SV,duplication_SV,out_name):
	out_deletion=open(out_name+'.deletion','w')	
	out_insertion=open(out_name+'.insertion','w')
	total=[]
	info={}
	for i in [clips_filter_SV,overlapping_filter_SV,indel_filter_SV,duplication_SV]:
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
		if total_sorted[x][3]=='DEL':
			out_deletion.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')
		elif total_sorted[x][3]=='INS':
			out_insertion.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')
