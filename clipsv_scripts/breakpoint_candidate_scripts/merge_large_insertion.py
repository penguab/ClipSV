#!/usr/bin/env python	
import sys,re

def merge_large_insertion(large_insertion,fold):
	out_file=open(large_insertion+".merge","w")
	def comp(para1,para2):
		line=para1.split('\t')
		region=para2.split('\t')
		if line[0]==region[0] and int(line[2])-int(region[2])<=20:
			if line[-1]=='1' or line[-2]=='1':
				region[2]=line[2]
			for i in [4,5,6,7,8,9,10,11,12]:
				region[i]=str(int(region[i])+int(line[i]))
			para2='\t'.join(region[0:])
		else:
			out=para2.split('\t')
			if int(out[5])>=fold and (int(out[9])>=fold or int(out[10])>=fold):
				out_file.write("\t".join([out[0],out[1],out[2],str(int(out[2])-int(out[1])),out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11]+':'+out[12]])+"\n")
			para2=para1
		return para2
	
	
	left=''
	right=''
	with open(large_insertion) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			direction=line[4].split(':')[1]
			if direction=='left':
				cont='\t'.join([line[0],line[1],line[2],line[3],line[-7],line[-6],line[-5],line[-4],line[-3],line[-2],line[-1],'1','0'])
			elif direction=='right':
				cont='\t'.join([line[0],line[1],line[2],line[3],line[-7],line[-6],line[-5],line[-4],line[-3],line[-2],line[-1],'0','1'])
			else:
				cont='\t'.join([line[0],line[1],line[2],line[3],line[-7],line[-6],line[-5],line[-4],line[-3],line[-2],line[-1],'0','0'])
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
		if int(out_left[5])>=fold and (int(out_left[9])>=fold or int(out_left[10])>=fold):
			out_file.write("\t".join([out_left[0],out_left[1],out_left[2],str(int(out_left[2])-int(out_left[1])),out_left[3],out_left[4],out_left[5],out_left[6],out_left[7],out_left[8],out_left[9],out_left[10],out_left[11]+':'+out_left[12]])+"\n")
	if right!='':
		out_right=right.split('\t')
		if int(out_right[5])>=fold and (int(out_right[9])>=fold or int(out_right[10])>=fold):
			out_file.write("\t".join([out_right[0],out_right[1],out_right[2],str(int(out_right[2])-int(out_right[1])),out_right[3],out_right[4],out_right[5],out_right[6],out_right[7],out_right[8],out_right[9],out_right[10],out_right[11]+':'+out_right[12]])+"\n")

if __name__ =="__main__":
	merge_large_insertion(sys.argv[1])

	
