#!/usr/bin/env python
import subprocess,sys	
def breakpoint_outINDEL(file1,file2,out):
	total=[]
	out_file=open(out,'w')
	command = subprocess.Popen(['bedtools','window','-a',file1,'-b',file2,'-w','100','-v'],stdout=subprocess.PIPE)
	while True:
		l= command.stdout.readline().decode('utf-8').rstrip()
		if not l:break
		line=l.split('\t')
		total.append(line)
	total_sort=sorted(total,key=lambda x: (x[0], int(x[1]),int(x[2])))
	for y in range(len(total_sort)):
		out_file.write(("\t".join(str(n) for n in total_sort[y]))+"\n")

if __name__=='__main__':
	breakpoint_outINDEL(sys.argv[1],sys.argv[2],sys.argv[3])

