#!/usr/bin/env python	
import sys,re
	
def merge_split_inversion(duplication,fold):	
	out_file=open(duplication+".merge","w")
	def comp(para1,para2):
		line=para1.split('\t')
		inside,overlap=0,0
		for i in range(len(para2)):
			region=para2[i].split('\t')
			if line[0]==region[0] and int(line[1])-int(region[1])<=5 and abs(int(line[2])-int(region[2]))<=5:
				region[1]=line[1]
				if int(line[2])-int(region[2])<0: 
					region[2]=line[2]
				for m in range(4,5):
					region[m]=str(int(region[m])+int(line[m]))
				para2[i]='\t'.join(region)
				inside=1
				break
			elif line[0]==region[0] and int(line[1])-int(region[1])<=5 and abs(int(line[2])-int(region[2]))>5:
				overlap=1
		if inside==0 and overlap==1:
			para2.append(para1)
		elif inside==0 and overlap==0:
			for x in range(len(para2)):
				out=para2[x].split('\t')
				if int(out[4])>=int(fold):
					out_file.write("\t".join([out[0],out[1],out[2],"INV",str(int(out[2])-int(out[1])),out[4]])+"\n")
			para2=[para1]
		return para2
	
	left,right=[],[]
	with open(duplication) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			cont='\t'.join([line[0],line[1],line[2],line[3]])+'\t1'
			if line[3]=='hp1':
				if len(left)==0:
					left=[cont]
					continue
				left=comp(cont,left)
			elif line[3]=='hp2':
				if len(right)==0:
					right=[cont]
					continue
				right=comp(cont,right)
	
	for x in range(len(left)):
		out=left[x].split('\t')
		if int(out[4])>=int(fold):
			out_file.write("\t".join([out[0],out[1],out[2],"INV",str(int(out[2])-int(out[1])),out[4]])+"\n")
	for x in range(len(right)):
		out=right[x].split('\t')
		if int(out[4])>=int(fold):
			out_file.write("\t".join([out[0],out[1],out[2],"INV",str(int(out[2])-int(out[1])),out[4]])+"\n")

if __name__=="__main__":
	merge_split_inversion(sys.argv[1],sys.argv[2])

	
