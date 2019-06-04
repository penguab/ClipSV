#!/usr/bin/env python	
import sys
	
def merge_bed(bed):
	out_file=open(bed+".merge","w")
	def comp(para1,para2):
		line=para1.split('\t')
		region=para2.split('\t')
		if line[0]==region[0] and int(line[2])-int(region[2])<=200:
			region[2]=line[2]
			para2='\t'.join(region[0:])
		else:
			out_file.write(para2+"\n")
			para2=para1
		return para2
	
	
	left=''
	with open(bed) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			cont='\t'.join([line[0],line[1],line[2]])
			if len(left)==0	:
				left=cont
				continue
			else:
				left=comp(cont,left)
	
	if left!='':
		out_file.write(left+"\n")
	
if __name__=="__main__":
	bed=sys.argv[1]
	merge_bed(bed)

