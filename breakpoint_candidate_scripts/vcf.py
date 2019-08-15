#!/usr/bin/env python	
import subprocess,sys,re,glob,os

def vcf(chromosome):
	SV_out=open("Candidate_SV.vcf","w")
	INDEL_out=open("Candidate_INDEL.vcf","w")
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
	f5=open("combined_SV.insertion.unique",'r')
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
	for y in range(len(SV_sort)):
		if SV_sort[y][3]=="DEL":
			SV_out.write(SV_sort[y][0]+"\t"+SV_sort[y][1]+"\t.\t.\t.\t.\t.\t"+"SVTYPE=DEL;SVLEN="+SV_sort[y][4]+"\tGT\n")
		elif SV_sort[y][3]=="INS":
			SV_out.write(SV_sort[y][0]+"\t"+SV_sort[y][1]+"\t.\t.\t.\t.\t.\t"+"SVTYPE=INS;SVLEN="+SV_sort[y][4]+"\tGT\n")
		elif SV_sort[y][3]=="INV":
			SV_out.write(SV_sort[y][0]+"\t"+SV_sort[y][1]+"\t.\t.\t.\t.\t.\t"+"SVTYPE=INV;SVLEN="+SV_sort[y][4]+"\tGT\n")
		elif SV_sort[y][3]=="TRANS":
			SV_out.write(SV_sort[y][0]+"\t"+SV_sort[y][1]+"\t.\t.\t"+SV_sort[y][4]+"\t.\t.\t"+"SVTYPE=TRANS;SVLEN=-"+"\tGT\n")
	INDEL_sort=sorted(INDEL,key=lambda x: (x[0], int(x[1])))
	for y in range(len(INDEL_sort)):
		if INDEL_sort[y][3]=="DEL":
			INDEL_out.write(INDEL_sort[y][0]+"\t"+INDEL_sort[y][1]+"\t.\t.\t.\t.\t.\t"+"TYPE=DEL;LEN="+INDEL_sort[y][4]+"\tGT\n")
		elif INDEL_sort[y][3]=="INS":
			INDEL_out.write(INDEL_sort[y][0]+"\t"+INDEL_sort[y][1]+"\t.\t.\t.\t.\t.\t"+"TYPE=INS;LEN="+INDEL_sort[y][4]+"\tGT\n")

if __name__=="__main__":
	vcf(sys.argv[1:])
