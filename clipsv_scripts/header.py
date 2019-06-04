#!/usr/bin/env python
import subprocess

def header(bam):
	command=subprocess.Popen(['samtools','view','-H',bam], stdout=subprocess.PIPE)
	chromosomes=[]
	while True:
		l= command.stdout.readline().decode('utf-8').rstrip()
		if not l: break
		line=l.split('\t')
		if line[0]!="@SQ":
			continue
		length=line[2].split(':')[1]
		if int(length)<=40000000:
			continue
		name=line[1].split(':')[1]
		chromosomes.append(name)
	return chromosomes

