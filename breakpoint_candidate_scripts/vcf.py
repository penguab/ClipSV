#!/usr/bin/env python	
import subprocess,sys,re,glob,os

def vcf(chromosome):
	SV_out=open("Candidate_SV.vcf","w")
	INDEL_out=open("Candidate_INDEL.vcf","w")
	SV=[]
	INDEL=[]
	f1=open("Candidate_SV.outBlacklist.bed",'r')
	while True:
		l=f1.readline().rstrip()
		if not l: break
		line=l.split('\t')
		if line[3]=="DEL":
			SV_out.write(line[0]+"\t"+line[1]+"\t.\t.\t.\t.\t.\t"+"SVTYPE=DEL;SVLEN="+line[4]+"\tGT\n")
		elif line[3]=="INS":
			SV_out.write(line[0]+"\t"+line[1]+"\t.\t.\t.\t.\t.\t"+"SVTYPE=INS;SVLEN="+line[4]+"\tGT\n")
		elif line[3]=="DUP":
			SV_out.write(line[0]+"\t"+line[1]+"\tDUP\t.\t.\t.\t.\t"+"SVTYPE=INS;SVLEN="+line[4]+"\tGT\n")
		elif line[3]=="INV":
			SV_out.write(line[0]+"\t"+line[1]+"\t.\t.\t.\t.\t.\t"+"SVTYPE=INV;SVLEN="+line[4]+"\tGT\n")
		elif line[3]=="TRANS":
			SV_out.write(line[0]+"\t"+line[1]+"\t.\t.\t"+line[4]+"\t.\t.\t"+"SVTYPE=TRANS;SVLEN=-"+"\tGT\n")
	f1.close()
	f2=open("Candidate_INDEL.outBlacklist.bed",'r')
	while True:
		l=f2.readline().rstrip()
		if not l: break
		line=l.split("\t")
		if line[3]=="DEL":
			INDEL_out.write(line[0]+"\t"+line[1]+"\t.\t.\t.\t.\t.\t"+"TYPE=DEL;LEN="+line[4]+"\tGT\n")
		elif line[3]=="INS":
			INDEL_out.write(line[0]+"\t"+line[1]+"\t.\t.\t.\t.\t.\t"+"TYPE=INS;LEN="+line[4]+"\tGT\n")
	f2.close()

if __name__=="__main__":
	vcf(sys.argv[1:])
