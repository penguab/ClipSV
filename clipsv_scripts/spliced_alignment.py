#!/usr/bin/env python
import subprocess,sys,os

def spliced_alignment(chromosome,bam,genome):
	path=os.getcwd()
	os.chdir(chromosome+"_dir")
	devnull=open(os.devnull, 'w')
	clips=chromosome+"_clips"
	clips_bam=clips+".sorted_name.bam"
	subprocess.call(['samtools','sort','-n',clips,'-o',clips_bam],stdout=devnull, stderr=devnull)
	samtools_fastq_command=subprocess.Popen(['samtools','fastq','-0','/dev/null','-F','0x900',clips_bam], stdout=subprocess.PIPE,stderr=devnull)
	samtools_fastq=clips_bam+".fastq"
	samtools_fastq_file=open(samtools_fastq,'w')
	samtools_fastq_file.write(samtools_fastq_command.stdout.read().decode('utf-8'))
	samtools_fastq_file.close()
	minimap2_command=subprocess.Popen(['minimap2','-ax','splice',genome,samtools_fastq], stdout=subprocess.PIPE,stderr=devnull)
	minimap2_out=samtools_fastq+".minimap2"
	minimap2_out_file=open(minimap2_out,'w')
	minimap2_out_file.write(minimap2_command.stdout.read().decode('utf-8'))
	minimap2_out_file.close()
	from breakpoint_candidate_scripts.minimap2_sv import minimap2_sv
	minimap2_sv(minimap2_out)
	from breakpoint_candidate_scripts.clips_filter import clips_filter
	clips_filter(chromosome, minimap2_out+'.sv')
	from breakpoint_candidate_scripts.remove_redundancy import remove_redundancy
	remove_redundancy(clips+'.filter.DEL')
	os.chdir(path)

if __name__ == "__main__":
	chromosome,bam,genome=sys.argv[1:]
	breakpoint_candidate(chromosome,bam,genome)

