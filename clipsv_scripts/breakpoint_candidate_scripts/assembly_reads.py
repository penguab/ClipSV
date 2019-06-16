#!/usr/bin/env python	
import subprocess,sys,re
def assembly_reads(chromosome,bed,bam):	
	out_file=open(chromosome+"_reads_name","w")
	clip_p=re.compile(r'^\d+([MSH])(\d+[MDI])*\d+([MSH])$')
	def bx_info(para1,para2):
		out = subprocess.Popen(['samtools','view',bam,para1,para2],stdout=subprocess.PIPE)
		name=[]
		while True:
			line = out.stdout.read()
			if not line:break
			for array in line.decode('utf-8').split('\n'):
				if not array: continue
				cont=array.split('\t')
				if int(cont[1])%2048>=1024 : continue
				if int(cont[4])<20: continue
				if int(cont[1])%4 <2 :
					name.append(cont[0])
					continue
				m=clip_p.search(cont[5])
				if not m: continue
				if m.group(1)!="M" or m.group(3)!="M":
					name.append(cont[0])
		out.communicate()
		return set(name)
	
	with open(bed) as f1:
		while True:
			line = f1.readline().rstrip()
			if not line: break
			if line[0]=="#":continue
			cont = line.split('\t')
			chro=cont[0]
			start1=int(cont[1])-500
			end1=int(cont[1])+700
			para1 = chro+':'+str(start1)+'-'+str(end1)
			start2=int(cont[2])-500
			end2=int(cont[2])+700
			para2 = chro+':'+str(start2)+'-'+str(end2)
			out = bx_info(para1,para2) 
			out_file.write("\t".join([chro,cont[1],cont[2],"INS","-",str(len(out)),(";").join(out)])+"\n")
	
