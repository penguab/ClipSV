#!/usr/bin/env python	
import subprocess,sys,re,glob,os

def contig_pool(path):
	os.chdir(path)
	out_file=open("contig_all.fa","w")
	files=glob.glob(path+"/assembly/*ass/velveth_*/contigs.fa",recursive=True)
	for name in files:
		m=re.search(r".*/assembly/(.*).ass/velveth_(.*)/contigs.fa",name)
		f=open(name,'r')
		while True:
			l=f.readline().rstrip()
			if not l: break
			if re.match(r"^>",l):
				out_file.write(l+"_"+m.group(1)+"_"+m.group(2)+"\n")
			else:
				out_file.write(l+"\n")
		f.close()


