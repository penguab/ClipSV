#!/usr/bin/env python
import sys,re

def Masked_genome(genome,chro):
	out=open('blacklist.bed','a')
	g= open(genome,'r')
	info={}
	chromosome=[]
	cont=g.read().split('>')
	del cont[0]
	for i in range(len(cont)):
		m=re.search(r'^([^\n]*)\n([\s\S]*)',cont[i],re.M)
		if m:
			chromosome.append(m.group(1).split(" ")[0])
			info[m.group(1).split(" ")[0]]=m.group(2).replace('\n','').lower()
		else:
			exit("could not find ref sequence for \n"+cont[i]+"\n!\n")
	nucleotide=['A','T','C','G','a','t','c','g']
	for n in range(len(chromosome)):
		if chromosome[n]!=chro:
			continue
		start,end=-1,-1
		for m in range(len(info[chromosome[n]])):
			if info[chromosome[n]][m] not in nucleotide:
				if start==-1:
					start=m
					end=m+1
					continue
				if m-end>1000:
					out.write('\t'.join([chromosome[n],str(start),str(end),str(end-start)])+'\tNNNregion\n')
					start=m
					end=m+1
				else:
					end=m+1
		if start!=-1:
			out.write('\t'.join([chromosome[n],str(start),str(end),str(end-start)])+'\tNNNregion\n')

if __name__=="__main__":
	Masked_genome(sys.argv[1],sys.argv[2])

