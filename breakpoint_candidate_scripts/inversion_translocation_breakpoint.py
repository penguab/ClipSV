#!/usr/bin/env python	
import subprocess,sys,re,glob,os

def inversion_translocation_breakpoint():
	SV_out=open("inversion_translocation.breakpoint","w")
	SV=[]
	f6=open("inversion_total",'r')
	while True:
		l=f6.readline().rstrip()
		if not l: break
		line=l.split("\t")
		SV.append([line[0],line[1],str(int(line[1])+1)])
		SV.append([line[0],line[2],str(int(line[2])+1)])
	f6.close()
	f7=open("translocation_total",'r')
	while True:
		l=f7.readline().rstrip()
		if not l: break
		line=l.split("\t")
		SV.append([line[0],line[1],str(int(line[1])+1)])
	f7.close()
	SV_sort=sorted(SV,key=lambda x: (x[0], int(x[1])))
	for x in range(len(SV_sort)):
		SV_out.write(('\t'.join(str(n) for n in SV_sort[x]))+'\n')

if __name__=="__main__":
	inversion_translocation_breakpoint()

