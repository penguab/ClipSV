#!/usr/bin/env python	
import sys,re
	
def merge_inversion_pair(inversion_pair,fold):	
	out_file=open(inversion_pair+".merge","w")
	def comp(para1,para2):
		line=para1.split('\t')
		inside,overlap=0,0
		for i in range(len(para2)):
			region=para2[i].split('\t')
			if line[0]==region[0] and int(line[1])-int(region[1])<=400 and abs(int(line[2])-int(region[2]))<=400:
				if line[4]=='1':
					region[1]=line[1]
				if line[5]=='1':
					region[2]=line[2]
				for m in range(4,7):
					region[m]=str(int(region[m])+int(line[m]))
				if region[4]=='0':
					region[1]=line[1]
				if region[5]=='0' and int(line[2])-int(region[2])>0: 
					region[2]=line[2]
				para2[i]='\t'.join(region)
				inside=1
				break
			elif line[0]==region[0] and int(line[1])-int(region[1])<=400 and abs(int(line[2])-int(region[2]))>400:
				overlap=1
		if inside==0 and overlap==1:
			para2.append(para1)
		elif inside==0 and overlap==0:
			for x in range(len(para2)):
				out=para2[x].split('\t')
				if int(out[4])+int(out[5])>=int(fold) and int(out[6])>=int(fold):
					out_file.write("\t".join([out[0],out[1],out[2],"INV",str(int(out[2])-int(out[1]))])+"\n")
			para2=[para1]
		return para2
	
	left,right=[],[]
	with open(inversion_pair) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			if line[4]=="left":
				cont='\t'.join([line[0],line[1],line[2],line[3],'1','0','1'])
			elif line[4]=="right":
				cont='\t'.join([line[0],line[1],line[2],line[3],'0','1','1'])
			elif line[4]=="NA":
				cont='\t'.join([line[0],line[1],line[2],line[3],'0','0','1'])
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
		if int(out[4])+int(out[5])>=int(fold) and int(out[6])>=int(fold):
			out_file.write("\t".join([out[0],out[1],out[2],"INV",str(int(out[2])-int(out[1]))])+"\n")
	for x in range(len(right)):
		out=right[x].split('\t')
		if int(out[4])+int(out[5])>=int(fold) and int(out[6])>=int(fold):
			out_file.write("\t".join([out[0],out[1],out[2],"INV",str(int(out[2])-int(out[1]))])+"\n")

if __name__=="__main__":
	merge_inversion_pair(sys.argv[1],sys.argv[2])

	
