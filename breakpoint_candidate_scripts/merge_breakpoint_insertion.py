#!/usr/bin/env python	
def merge_breakpoint_insertion(breakpoint_outDEL):
	out_file=open(breakpoint_outDEL+".insertion","w")
	def comp(para1,para2):
		line=para1.split('\t')
		region=para2.split('\t')
		if line[0]==region[0] and int(line[2])-int(region[2])<=200:
			region[2]=line[2]
			for i in [4,5,6,7,8,9,10,11,12]:
				region[i]=str(int(region[i])+int(line[i]))
			para2='\t'.join(region[0:])
		else:
			out=para2.split('\t')
			if int(out[11])>=1 and int(out[12])>=1:
				out_file.write("\t".join([out[0],out[1],out[2],"INS","-"])+"\n")
			para2=para1
		return para2
	
	
	left=''
	right=''
	with open(breakpoint_outDEL) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			if int(line[13])>=1 and int(line[14])>=1:
				continue
			cont='\t'.join([line[0],line[1],line[2],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[13],line[14]])
			if line[4]=='hp1':
				if len(left)==0	:
					left=cont
					continue
				else:
					left=comp(cont,left)
			elif line[4]=='hp2':
				if len(right)==0 :
					right=cont
					continue
				else:
					right=comp(cont,right)
	
	if left!='':
		out_left=left.split('\t')
		if int(out_left[11])>=1 and int(out_left[12])>=1:
			out_file.write("\t".join([out_left[0],out_left[1],out_left[2],"INS","-"])+"\n")
	if right!='':
		out_right=right.split('\t')
		if int(out_right[11])>=1 and int(out_right[12])>=1:
			out_file.write("\t".join([out_right[0],out_right[1],out_right[2],"INS","-"])+"\n")
	
