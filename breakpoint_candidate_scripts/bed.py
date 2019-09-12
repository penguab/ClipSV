#!/usr/bin/env python	
import subprocess,sys,re,glob,os

def bed(chromosome):
	SV_out=open("Candidate_SV.bed","w")
	INDEL_out=open("Candidate_INDEL.bed","w")
	SV=[]
	INDEL=[]
	f1=open("combined_INDEL.unique",'r')
	while True:
		l=f1.readline().rstrip()
		if not l: break
		INDEL.append(l.split("\t"))
	f1.close()
	f2=open("contig_all.minimap.splice.sam.sv.INS",'r')
	while True:
		l=f2.readline().rstrip()
		if not l: break
		line=l.split("\t")
		if line[4]=="-" or int(line[4])>=50:
			SV.append(line)
		else:
			INDEL.append(line)
	f2.close()
	f3=open("combined_SV.deletion.unique",'r')
	while True:
		l=f3.readline().rstrip()
		if not l: break
		SV.append(l.split("\t"))
	f3.close()
	f5=open("insertion_total",'r')
	while True:
		l=f5.readline().rstrip()
		if not l: break
		SV.append(l.split("\t"))
	f5.close()
	f6=open("inversion_total",'r')
	while True:
		l=f6.readline().rstrip()
		if not l: break
		SV.append(l.split("\t"))
	f6.close()
	f7=open("translocation_total",'r')
	while True:
		l=f7.readline().rstrip()
		if not l: break
		SV.append(l.split("\t"))
	f7.close()
	SV_sort=sorted(SV,key=lambda x: (x[0], int(x[1])))
	for x in range(len(SV_sort)):
		SV_out.write(("\t".join(str(n) for n in SV_sort[x][0:5]))+"\n")
	INDEL_sort=sorted(INDEL,key=lambda x: (x[0], int(x[1])))
	for y in range(len(INDEL_sort)):
		INDEL_out.write(("\t".join(str(n) for n in INDEL_sort[y][0:5]))+"\n")

if __name__=="__main__":
	bed(sys.argv[1:])
