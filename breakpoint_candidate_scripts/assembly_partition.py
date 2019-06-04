#!/usr/bin/env python	
import os,shutil,subprocess,sys,re
def assembly_partition(name,bam):	
	left,right,All={},{},{}
	total=[]
	with open(name) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			line=l.split("\t")
			if int(line[5])<=5 or int(line[5])>=2000: continue
			barcode3=line[-1].split(";")
			for m in range(len(barcode3)):
				try:
					All[barcode3[m]].append("HPall_"+line[0]+"_"+line[1]+"_"+line[2]+"_"+line[3]+"_"+line[4])
					total.append("HPall_"+line[0]+"_"+line[1]+"_"+line[2]+"_"+line[3]+"_"+line[4])
				except KeyError:
					All[barcode3[m]]=[]
					All[barcode3[m]].append("HPall_"+line[0]+"_"+line[1]+"_"+line[2]+"_"+line[3]+"_"+line[4])
					total.append("HPall_"+line[0]+"_"+line[1]+"_"+line[2]+"_"+line[3]+"_"+line[4])
	
	output={}
	if os.path.isdir("assembly"):
		shutil.rmtree("assembly")
	os.mkdir("assembly")
	for x in set(total):
		output[x]=open("./assembly/"+x,'w')
	
	command= subprocess.Popen(['samtools','view','-h',bam], stdout=subprocess.PIPE)
	
	while True:
		l= command.stdout.readline().decode('utf-8').rstrip()
		if not l: break
		if l[0]=='@':
			for n in set(total):
				output[n].write(str(l)+"\n")
		line=l.split('\t')
		if line[0] in All:
			for i in range(len(All[line[0]])):
				output[All[line[0]][i]].write(str(l)+"\n")
	command.communicate()
	
	for y in set(total):
		output[y].close()

	
