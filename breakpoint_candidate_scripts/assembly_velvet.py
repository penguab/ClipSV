#!/usr/bin/env python	
import os,shutil,subprocess,glob
def assembly_velvet(path):
	current_path=path+"/assembly"
	os.chdir(current_path)
	files=glob.glob("HP*-")
	for f in files:
		try:
			shutil.rmtree(f+".ass")
		except:
			pass
		os.mkdir(f+".ass")
		os.chdir(f+".ass")
		devnull=open(os.devnull, 'w')
		subprocess.call(['samtools', 'sort', '-n','../'+f,'-o',f+'.sorted_name.bam'],stdout=devnull, stderr=devnull)
		subprocess.call(['samtools','fastq', '-1', 'paired_1.fastq', '-2', 'paired_2.fastq', '-0', '/dev/null', '-s', '/dev/null', '-n', '-F', '0x900', f+'.sorted_name.bam'],stdout=devnull, stderr=devnull)
		for x in ['41', '61', '81']:
			subprocess.call(['velveth', 'velveth_'+x, x, '-shortPaired', '-fastq', 'paired_1.fastq', 'paired_2.fastq'],stdout=devnull, stderr=devnull)
			subprocess.call(['velvetg', 'velveth_'+x, '-exp_cov', '10', '-ins_length', '500', '-min_contig_lgth', '200'],stdout=devnull, stderr=devnull)
		os.chdir(current_path)

	
