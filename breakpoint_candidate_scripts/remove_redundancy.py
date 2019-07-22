#!/usr/bin/env python	

import sys

def remove_redundancy(clips_DEL):
	output=open(clips_DEL+".unique",'w')
	def comp(para1,para2):
		line=para1.split('\t')
		inside,overlap=0,0
		for i in range(len(para2)):
			region=para2[i].split('\t')
			if float(line[4])/float(region[4])<=2 and float(line[4])/float(region[4])>=0.5:
				length_match=1
			else:
				length_match=0
			if line[3]==region[3] and int(line[1])-int(region[1])<=50 and length_match==1:
				if int(line[4])>int(region[4]):
					del para2[i]
					para2.append(para1)
				inside=1
				break
			elif line[3]==region[3] and int(line[1])-int(region[1])<=50 and length_match==0:
				overlap=1
		if inside==0 and overlap==1:
			para2.append(para1)
		elif inside==0 and overlap==0:
			for x in range(len(para2)):
				output.write(para2[x]+'\n')
			para2=[para1]
		return para2
	
	left=[]
	with open(clips_DEL) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			cont='\t'.join([line[0],line[1],line[2],line[3],line[4]])
			if len(left)==0:
				left=[cont]
				continue
			left=comp(cont,left)
	
	for x in range(len(left)):
		output.write(left[x]+'\n')
	
if __name__=='__main__':
	remove_redundancy(sys.argv[1])
