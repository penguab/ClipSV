#!/usr/bin/env python	
import sys,re
	
def inversion_pair(inversion,size,length):	
	out_file=open(inversion+".pair","w")
	total=[]
	with open(inversion) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			if line[4].split(':')[1]=='left' and int(line[12])-int(line[8])>int(size):
				end=str(int(line[8])+int(size)+int(line[12])-int(line[1]))
				total.append([line[0],line[1],end,line[3],"left",str(int(end)-int(line[1]))])
			elif line[4].split(':')[1]=='right' and int(line[12])-int(line[8])<-int(size):
				start=str(int(line[1])+int(line[4].split(':')[0])-int(size)-(int(line[1])-int(line[12])-int(length)))
				total.append([line[0],start,line[1],line[3],"right",str(int(line[1])-int(start))])
			elif line[4].split(':')[1]=='NA' and int(line[12])-int(line[8])>int(size):
				end=str(int(line[12])+int(length))
				total.append([line[0],line[8],end,line[3],"NA",str(int(end)-int(line[8]))])
			elif line[4].split(':')[1]=='NA' and int(line[12])-int(line[8])<-int(size):
				end=str(int(line[8])+int(length))
				total.append([line[0],line[12],end,line[3],"NA",str(int(end)-int(line[12]))])
	total_sorted=sorted(total,key=lambda x: (x[0], int(x[1]),int(x[2])))
	for x in range(len(total_sorted)):
		out_file.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')

if __name__=="__main__":
	inversion_pair(sys.argv[1],sys.argv[2],sys.argv[3])

	
