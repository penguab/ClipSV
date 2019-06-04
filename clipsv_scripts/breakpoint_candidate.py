#!/usr/bin/env python
import subprocess,sys,os

def breakpoint_candidate(chromosome,bam,genome):
	os.chdir(chromosome+"_dir")
	path=os.getcwd()
	clips=chromosome+"_clips"
	indel=chromosome+"_indel"
	from breakpoint_candidate_scripts.indel_filter import indel_filter
	indel_filter(indel)
	from breakpoint_candidate_scripts.indel_clips_total import indel_clips_total
	indel_clips_total(indel+".filter",clips+".filter.INDEL",indel+"_clips_INDEL")
	from breakpoint_candidate_scripts.remove_redundancy import remove_redundancy
	remove_redundancy(indel+"_clips_INDEL")
	breakpoint=chromosome+"_breakpoint"
	from breakpoint_candidate_scripts.breakpoint_sort import breakpoint_sort
	breakpoint_sort(breakpoint)
	from breakpoint_candidate_scripts.merge_breakpoint import merge_breakpoint
	merge_breakpoint(breakpoint+".sort")
	from breakpoint_candidate_scripts.breakpoint_filter import breakpoint_filter
	breakpoint_filter(breakpoint+".sort.merge")
	from breakpoint_candidate_scripts.breakpoint_outINDEL import breakpoint_outINDEL
	breakpoint_outINDEL(breakpoint+".sort.merge.filter",indel+"_clips_INDEL",breakpoint+".outINDEL")
	breakpoint_outINDEL(clips+'.filter.DEL.unique',indel+"_clips_INDEL.insertion",clips+'.filter.DEL.unique_outINDEL')
	from breakpoint_candidate_scripts.merge_bed import merge_bed
	merge_bed(breakpoint+".outINDEL")
	from breakpoint_candidate_scripts.split_duplication import split_duplication
	split=chromosome+"_split"
	split_duplication(split)
	from breakpoint_candidate_scripts.merge_split_duplication import merge_split_duplication
	merge_split_duplication(split+".duplication")
	from breakpoint_candidate_scripts.large_insertion_sort import large_insertion_sort
	large_insertion=chromosome+"_large_insertion"
	large_insertion_sort(large_insertion)
	from breakpoint_candidate_scripts.merge_large_insertion import merge_large_insertion
	merge_large_insertion(large_insertion+".sort")
	translocation=chromosome+"_translocation"
	large_insertion_sort(translocation)
	merge_large_insertion(translocation+".sort")
	from breakpoint_candidate_scripts.insertion_total import insertion_total
	insertion_total(clips+".filter.INS",split+".duplication.merge",large_insertion+".sort.merge",translocation+".sort.merge")
	breakpoint_outINDEL("insertion_total",indel+"_clips_INDEL","insertion_total.outINDEL")
	from breakpoint_candidate_scripts.assembly_reads import assembly_reads
	assembly_reads(chromosome,breakpoint+".outINDEL.merge",bam)
	from breakpoint_candidate_scripts.assembly_partition import assembly_partition
	assembly_partition(chromosome+"_reads_name",bam)
	from breakpoint_candidate_scripts.assembly_velvet import assembly_velvet
	assembly_velvet(path)
	from breakpoint_candidate_scripts.contig_pool import contig_pool
	contig_pool(path)
	devnull=open(os.devnull, 'w')
	contig_command=subprocess.Popen(['minimap2','-ax','splice',genome,'contig_all.fa'], stdout=subprocess.PIPE,stderr=devnull)
	contig_command_out_file=open("contig_all.minimap.splice.sam",'w')
	contig_command_out_file.write(contig_command.stdout.read().decode('utf-8'))	
	contig_command_out_file.close()
	from breakpoint_candidate_scripts.event_sv import event_sv
	event_sv("contig_all.minimap.splice.sam")
	from breakpoint_candidate_scripts.event_sv_INS import event_sv_INS
	event_sv_INS("contig_all.minimap.splice.sam.sv")
	breakpoint_outINDEL("insertion_total.outINDEL","contig_all.minimap.splice.sam.sv.INS","insertion_total.unassemblied")
	merge_bed("insertion_total.unassemblied")

if __name__ == "__main__":
	chromosome,bam,genome=sys.argv[1:]
	breakpoint_candidate(chromosome,bam,genome)

