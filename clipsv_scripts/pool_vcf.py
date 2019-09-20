#!/usr/bin/env python	
import subprocess,sys,re,glob,os

def pool_vcf(Chromosomes,prefix):
	path=os.getcwd()
	SV_out=open(prefix+"_ClipSV_Candidate_SV.vcf","w")
	INDEL_out=open(prefix+"_ClipSV_Candidate_INDEL.vcf","w")
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
	SV_out.write('##fileformat=VCFv4.2\n##source=ClipSV\n##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">\n##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">\n##INFO=<ID=BREAKPOINT,Number=.,Type=String,Description="Breakpoint of translocation">\n##ALT=<ID=DEL,Description="Deletion">\n##ALT=<ID=INS,Description="Insertion">\n##ALT=<ID=INV,Description="Inversion">\n##ALT=<ID=TRANS,Description="Translocation">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n##FORMAT=<ID=CR,Number=1,Type=Integer,Description="Number of clipped reads">\n##FORMAT=<ID=NR,Number=1,Type=Integer,Description="Number of non-clipped reads">\n')
	SV_out.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n")
	for y in range(len(SV_sort)):
		SV_out.write(("\t".join(str(n) for n in SV_sort[y]))+"\n")
	INDEL_sort=sorted(INDEL,key=lambda x: (x[0], int(x[1])))
	INDEL_out.write('##fileformat=VCFv4.2\n##source=ClipSV\n##INFO=<ID=TYPE,Number=1,Type=String,Description="Type of INDELs">\n##INFO=<ID=LEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">\n##ALT=<ID=DEL,Description="Deletion">\n##ALT=<ID=INS,Description="Insertion">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
	INDEL_out.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n")
	for y in range(len(INDEL_sort)):
		INDEL_out.write(("\t".join(str(n) for n in INDEL_sort[y]))+"\n")

if __name__=="__main__":
	print(sys.argv[1:])
	pool_vcf(sys.argv[1:])
