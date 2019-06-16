#!/usr/bin/env python	
import subprocess,sys,re,glob,os

def pool_vcf(Chromosomes):
	path=os.getcwd()
	SV_out=open("ClipSV_Candidate_SV.vcf","w")
	INDEL_out=open("ClipSV_Candidate_INDEL.vcf","w")
	SV=[]
	INDEL=[]
	for chromosome in Chromosomes:
		os.chdir(chromosome+"_dir")
		f1=open("Candidate_INDEL.vcf",'r')
		while True:
			l=f1.readline().rstrip()
			if not l: break
			INDEL.append(l.split("\t"))
		f1.close()
		f2=open("Candidate_SV.genotype.vcf",'r')
		while True:
			l=f2.readline().rstrip()
			if not l: break
			SV.append(l.split("\t"))
		f2.close()
		os.chdir(path)
	SV_sort=sorted(SV,key=lambda x: (x[0], int(x[1])))
	SV_out.write("##fileformat=VCFv4.2\n")
	SV_out.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n")
	for y in range(len(SV_sort)):
		SV_out.write(("\t".join(str(n) for n in SV_sort[y]))+"\n")
	INDEL_sort=sorted(INDEL,key=lambda x: (x[0], int(x[1])))
	INDEL_out.write("##fileformat=VCFv4.2\n")
	INDEL_out.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n")
	for y in range(len(INDEL_sort)):
		INDEL_out.write(("\t".join(str(n) for n in INDEL_sort[y]))+"\n")

if __name__=="__main__":
	print(sys.argv[1:])
	pool_vcf(sys.argv[1:])
