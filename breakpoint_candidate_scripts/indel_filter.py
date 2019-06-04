#!/usr/bin/env python	
import sys,re
	
def indel_filter(indel):
	out_sv=open(indel+'.over50bp','w')
	out=open(indel+'.filter','w')	
	out_total=open(indel+'.total','w')
	total,total_uniq=[],[]
	mark={}
	with open(indel) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			line=l.split('\t')
			if int(line[9])<0 : continue
			length=line[4].split(':')[0]
			if line[4].split(':')[1]=="D":
				total.append("\t".join([line[0],line[1],str(int(line[1])+int(length)+1),"DEL",length]))
			elif line[4].split(':')[1]=="I":
				total.append("\t".join([line[0],line[1],str(int(line[1])+1),"INS",length]))
	for i in range(len(total)):
		if total[i] in mark:
			mark[total[i]]+=1
		else:
			mark[total[i]]=1
	for name in mark:
		if mark[name]>=2:
			total_uniq.append(name.split('\t'))
	total_sort=sorted(total_uniq,key=lambda x: (x[0], int(x[1]),x[3]))
	for y in range(len(total_sort)):
		if int(total_sort[y][4])>=50:
			out_sv.write(("\t".join(str(n) for n in total_sort[y]))+"\n")
		else:
			out_total.write(("\t".join(str(n) for n in total_sort[y]))+"\n")
			if int(total_sort[y][4])>=5:
				out.write(("\t".join(str(n) for n in total_sort[y]))+"\n")

if __name__=="__main__":
	indel=sys.argv[1]
	indel_filter(indel)

