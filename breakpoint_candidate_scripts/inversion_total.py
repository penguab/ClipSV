#!/usr/bin/env python
import subprocess,sys	
def inversion_total(pair_merge,split_merge):
	total=[]
	out_file=open("inversion_total",'w')
	command = subprocess.Popen(['bedtools','window','-a',pair_merge,'-b',split_merge,'-w','100','-v'],stdout=subprocess.PIPE)
	while True:
		l= command.stdout.readline().decode('utf-8').rstrip()
		if not l:break
		line=l.split('\t')
		total.append(line[0:5])
	with open(split_merge) as f:
		while True:
			l=f.readline().rstrip()
			if not l:break
			line=l.split('\t')
			total.append(line[0:5])
	total_sort=sorted(total,key=lambda x: (x[0], int(x[1]),int(x[2])))
	for y in range(len(total_sort)):
		out_file.write(("\t".join(str(n) for n in total_sort[y]))+"\n")

if __name__=='__main__':
	inversion_total(sys.argv[1],sys.argv[2])

