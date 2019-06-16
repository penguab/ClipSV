#!/usr/bin/env python
import subprocess,re,sys
from math import sqrt
def insert_size(bam,chr1,chr2,chr3):
	def stddev(lst):
		mean = float(sum(lst)) / len(lst)
		return mean, sqrt(sum((x - mean)**2 for x in lst) / (len(lst)-1))

	para1=chr1+':20000000-21000000'
	para2=chr2+':20000000-21000000'
	para3=chr3+':20000000-21000000'
	size=[]
	number=0
	length='0'
	out = subprocess.Popen(['samtools','view',bam,para1,para2,para3],stdout=subprocess.PIPE)
	while True:
		line = out.stdout.read()
		if not line:break
		for array in line.decode('utf-8').split('\n'):
			if not array: continue
			cont=array.split('\t')
			if int(cont[1])%2048>=1024 or int(cont[1])>=2048 or int(cont[1])%512>=256:continue
			number+=1
			if int(cont[1])%4<2 or int(cont[4])<60 : continue
			size.append(abs(int(cont[8])))
			m=re.search(r'^(\d+)M$',cont[5])
			if m:
				if int(length)< int(m.group(1)):
					length=m.group(1)
	coverage=int(number*int(length)/3000000)
	fold=int(round(float(coverage)/10))
	mean,sd=stddev(size)
	min_insert_size=max(int(mean-200),int(mean-int(sd)))
	max_insert_size=min(int(mean+200),int(mean+int(sd)))
	return min_insert_size,max_insert_size,int(length),fold
	
if __name__=="__main__":
	min_insert_size,max_insert_size,length,coverage=insert_size(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	print(min_insert_size,max_insert_size,length,coverage)
