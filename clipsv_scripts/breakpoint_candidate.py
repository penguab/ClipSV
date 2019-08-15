#!/usr/bin/env python
import subprocess,sys,os

def breakpoint_candidate(chromosome,bam,genome,fold,min_insert_size,max_insert_size,read_length):
	root_path=os.getcwd()
	os.chdir(chromosome+"_dir")
	path=os.getcwd()
	clips=chromosome+"_clips"
	indel=chromosome+"_indel"
	overlapping=chromosome+"_clips_overlapping"
	from breakpoint_candidate_scripts.indel_filter import indel_filter
	indel_filter(indel,int(fold))
	from breakpoint_candidate_scripts.combine_SV import combine_SV
	combine_SV(clips+".filter.SV",overlapping+".filter.SV",indel+".filter.SV","combined_SV")
	from breakpoint_candidate_scripts.combine_indel import combine_indel
	combine_indel(clips+".filter.INDEL",overlapping+".filter.INDEL",indel+".filter.INDEL","combined_INDEL")
	from breakpoint_candidate_scripts.remove_redundancy import remove_redundancy
	remove_redundancy("combined_INDEL")
	remove_redundancy("combined_SV.deletion")
	remove_redundancy("combined_SV.insertion")
	breakpoint=chromosome+"_breakpoint"
	from breakpoint_candidate_scripts.breakpoint_sort import breakpoint_sort
	breakpoint_sort(breakpoint)
	from breakpoint_candidate_scripts.merge_breakpoint import merge_breakpoint
	merge_breakpoint(breakpoint+".sort")
	from breakpoint_candidate_scripts.breakpoint_filter import breakpoint_filter
	breakpoint_filter(breakpoint+".sort.merge",int(fold))
	from breakpoint_candidate_scripts.breakpoint_outINDEL import breakpoint_outINDEL
	breakpoint_outINDEL(breakpoint+".sort.merge.filter","combined_INDEL",breakpoint+".outINDEL")
	from breakpoint_candidate_scripts.merge_bed import merge_bed
	merge_bed(breakpoint+".outINDEL")
	from breakpoint_candidate_scripts.split_duplication import split_duplication
	split=chromosome+"_split"
	split_duplication(split)
	from breakpoint_candidate_scripts.merge_split_duplication import merge_split_duplication
	merge_split_duplication(split+".duplication",int(fold))
	from breakpoint_candidate_scripts.large_insertion_sort import large_insertion_sort
	large_insertion=chromosome+"_large_insertion"
	large_insertion_sort(large_insertion)
	from breakpoint_candidate_scripts.merge_large_insertion import merge_large_insertion
	merge_large_insertion(large_insertion+".sort",int(fold))
	translocation=chromosome+"_translocation"
	large_insertion_sort(translocation)
	merge_large_insertion(translocation+".sort",int(fold))
	from breakpoint_candidate_scripts.insertion_total import insertion_total
	insertion_total("combined_SV.insertion.unique",split+".duplication.merge",large_insertion+".sort.merge",translocation+".sort.merge")
	breakpoint_outINDEL("insertion_total","combined_INDEL","insertion_total.outINDEL")
	breakpoint_outINDEL(breakpoint+".outINDEL.merge","insertion_total.outINDEL",breakpoint+".outINDEL.merge.outINS")
	breakpoint_outINDEL(breakpoint+".outINDEL.merge.outINS","combined_SV.deletion.unique",breakpoint+".outINDEL.merge.outINS.outDEL")
	from breakpoint_candidate_scripts.assembly_reads import assembly_reads
	assembly_reads(chromosome,breakpoint+".outINDEL.merge.outINS.outDEL",bam)
	from breakpoint_candidate_scripts.assembly_partition import assembly_partition
	assembly_partition(chromosome+"_reads_name",bam)
	from breakpoint_candidate_scripts.assembly_velvet import assembly_velvet
	assembly_velvet(path)
	from breakpoint_candidate_scripts.contig_pool import contig_pool
	contig_pool(path)
	devnull=open(os.devnull, 'w')
	contig_command=subprocess.Popen(['minimap2','-a',genome,'contig_all.fa'], stdout=subprocess.PIPE,stderr=devnull)
	contig_command_out_file=open("contig_all.minimap.splice.sam",'w')
	contig_command_out_file.write(contig_command.stdout.read().decode('utf-8'))	
	contig_command_out_file.close()
	from breakpoint_candidate_scripts.event_sv import event_sv
	event_sv("contig_all.minimap.splice.sam")
	from breakpoint_candidate_scripts.event_sv_INS import event_sv_INS
	event_sv_INS("contig_all.minimap.splice.sam.sv")
	from breakpoint_candidate_scripts.split_inversion import split_inversion
	split_inversion(split)
	from breakpoint_candidate_scripts.merge_split_inversion import merge_split_inversion
	merge_split_inversion(split+".inversion",fold)
	from breakpoint_candidate_scripts.inversion_pair import inversion_pair
	inversion_pair(chromosome+"_inversion",max_insert_size,read_length)
	from breakpoint_candidate_scripts.merge_inversion_pair import merge_inversion_pair
	merge_inversion_pair(chromosome+"_inversion.pair",fold)
	from breakpoint_candidate_scripts.inversion_total import inversion_total
	inversion_total(chromosome+"_inversion.pair.merge",chromosome+"_split.inversion.merge")
	from breakpoint_candidate_scripts.translocation_site import translocation_site
	translocation_site(chromosome+"_translocation.sort")
	from breakpoint_candidate_scripts.merge_translocation_site import merge_translocation_site
	merge_translocation_site(chromosome+"_translocation.sort.site",fold)
	from breakpoint_candidate_scripts.vcf import vcf
	vcf(chromosome)
	from breakpoint_candidate_scripts.genotype import genotype
	genotype("Candidate_SV.vcf",bam,min_insert_size,max_insert_size)
	os.chdir(root_path)

if __name__ == "__main__":
	chromosome,bam,genome=sys.argv[1:]
	breakpoint_candidate(chromosome,bam,genome)

