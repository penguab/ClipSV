#!/usr/bin/env python	
import sys,re
	
def merge_breakpoint(breakpoint):
	out_file=open(breakpoint+".merge",'w')
	def comp(para1,para2):
		line=para1.split('\t')
		region=para2.split('\t')
		match=0
		if line[0]==region[0] and int(line[2])-int(region[2])<=20:
			if line[-2]!='-':
				if region[-2]=='-':
					region[-2]=line[-2]
				else:
					seq=region[-2].split(';')
					for i in range(len(seq)):
						if len(line[-2])<len(seq[i]):
							shortseq=line[-2]
							longseq=seq[i]
						else:
							longseq=line[-2]
							shortseq=seq[i]
						index=longseq.find(shortseq)
						if index >=0 and index <=4:
							region[14]=str(int(region[14])+int(line[14]))
							match=1
							seq[i]=longseq
					if match!=1:
						region[-2]=line[-2]+";"+region[-2]
					else:
						region[-2]=';'.join(seq)
			if line[-1]!='-':
				if region[-1]=='-':
					region[-1]=line[-1]
				else:
					seq=region[-1].split(';')
					for i in range(len(seq)):
						if len(line[-1])<len(seq[i]):
							shortseq=line[-1]
							longseq=seq[i]
						else:
							longseq=line[-1]
							shortseq=seq[i]
						index=longseq.find(shortseq)
						if index >=0 and abs(index+len(shortseq)-len(longseq)) <=4:
							region[15]=str(int(region[15])+int(line[15]))
							match=1
							seq[i]=longseq
					if match!=1:
						region[-1]=line[-1]+";"+region[-1]
					else:
						region[-1]=';'.join(seq)
			region[2]=line[2]
			for i in [4,5,6,7,8,9,10,11,12,13]:
				region[i]=str(int(region[i])+int(line[i]))
			para2='\t'.join(region[0:])
		else:
			out=para2.split('\t')
			out_file.write("\t".join([out[0],out[1],out[2],str(int(out[2])-int(out[1])),out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11]+':'+out[12]+':'+out[13],out[14],out[15],out[16],out[17]])+"\n")
			para2=para1
		return para2
	
	
	left=''
	right=''
	with open(breakpoint) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			line[2]=str(int(line[1])+1)
			if int(line[9])>=60:
				mark='1'
			else:
				mark='0'
			m=re.search(r':(.*)$',line[4])
			if m.group(1)=='left':
				cont='\t'.join([line[0],line[1],line[2],line[3],line[-7],line[-6],line[-5],line[-4],line[-3],line[-2],line[-1],'1','0',mark,'1','0',line[-8].split(':')[-1],'-'])
			elif m.group(1)=='right':
				cont='\t'.join([line[0],line[1],line[2],line[3],line[-7],line[-6],line[-5],line[-4],line[-3],line[-2],line[-1],'0','1',mark,'0','1','-',line[-8].split(':')[-1]])
			if line[3]=='hp1':
				if len(left)==0	:
					left=cont
					continue
				else:
					left=comp(cont,left)
			elif line[3]=='hp2':
				if len(right)==0 :
					right=cont
					continue
				else:
					right=comp(cont,right)
	
	if left!='':
		out_left=left.split('\t')
		out_file.write("\t".join([out_left[0],out_left[1],out_left[2],str(int(out_left[2])-int(out_left[1])),out_left[3],out_left[4],out_left[5],out_left[6],out_left[7],out_left[8],out_left[9],out_left[10],out_left[11]+':'+out_left[12]+':'+out_left[13],out_left[14],out_left[15],out_left[16],out_left[17]])+"\n")
	if right!='':
		out_right=right.split('\t')
		out_file.write("\t".join([out_right[0],out_right[1],out_right[2],str(int(out_right[2])-int(out_right[1])),out_right[3],out_right[4],out_right[5],out_right[6],out_right[7],out_right[8],out_right[9],out_right[10],out_right[11]+':'+out_right[12]+':'+out_right[13],out_right[14],out_right[15],out_right[16],out_right[17]])+"\n")


	
