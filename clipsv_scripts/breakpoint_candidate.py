#!/usr/bin/env python
import subprocess,sys,os,shutil

def breakpoint_candidate(chromosome,bam,genome_fa,genome_mmi,coverage,min_insert_size,max_insert_size,read_length):
	fold=int(round(float(coverage)/10))
	root_path=os.getcwd()
	os.chdir(chromosome+"_dir")
	path=os.getcwd()
	clips=chromosome+"_clips"
	indel=chromosome+"_indel"
	overlapping=chromosome+"_clips_overlapping"
	from breakpoint_candidate_scripts.indel_filter import indel_filter
	indel_filter(indel,int(fold))
	split=chromosome+"_split"
	from breakpoint_candidate_scripts.split_duplication import split_duplication
	split_duplication(split)
	from breakpoint_candidate_scripts.merge_split_duplication import merge_split_duplication
	merge_split_duplication(split+".duplication",int(fold))
	from breakpoint_candidate_scripts.combine_SV import combine_SV
	combine_SV(clips+".filter.SV",overlapping+".filter.SV",indel+".filter.SV",split+".duplication.merge.SV","combined_SV")
	from breakpoint_candidate_scripts.combine_indel import combine_indel
	combine_indel(clips+".filter.INDEL",overlapping+".filter.INDEL",indel+".filter.INDEL",split+".duplication.merge.INDEL","combined_INDEL")
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
	translocation=chromosome+"_translocation"
	from breakpoint_candidate_scripts.large_insertion_sort import large_insertion_sort
	large_insertion_sort(translocation)
	from breakpoint_candidate_scripts.merge_large_insertion import merge_large_insertion
	merge_large_insertion(translocation+".sort",int(fold))
	from breakpoint_candidate_scripts.translocation_site import translocation_site
	translocation_site(chromosome+"_translocation.sort")
	from breakpoint_candidate_scripts.merge_translocation_site import merge_translocation_site
	merge_translocation_site(chromosome+"_translocation.sort.site",fold)
	from breakpoint_candidate_scripts.inversion_translocation_breakpoint import inversion_translocation_breakpoint
	inversion_translocation_breakpoint()
	large_insertion=chromosome+"_large_insertion"
	large_insertion_sort(large_insertion)
	merge_large_insertion(large_insertion+".sort",int(fold))
	breakpoint_outINDEL(chromosome+"_large_insertion.sort.merge","inversion_translocation.breakpoint","large_insertion.outInvTrans")
	breakpoint_outINDEL("large_insertion.outInvTrans","combined_SV.insertion.unique","large_insertion.outInvTrans.outInsertion")
	breakpoint_outINDEL(chromosome+"_translocation.sort.merge","inversion_translocation.breakpoint","translocation.outInvTrans")
	breakpoint_outINDEL("translocation.outInvTrans","combined_SV.insertion.unique","translocation.outInvTrans.outInsertion")
	from breakpoint_candidate_scripts.insertion_total import insertion_total
	insertion_total("combined_SV.insertion.unique","large_insertion.outInvTrans.outInsertion","translocation.outInvTrans.outInsertion")
	breakpoint_outINDEL("insertion_total","combined_INDEL","insertion_total.outINDEL")
	breakpoint_outINDEL(breakpoint+".outINDEL.merge","inversion_translocation.breakpoint",breakpoint+".outINDEL.merge.outInvTrans")
	breakpoint_outINDEL(breakpoint+".outINDEL.merge.outInvTrans","insertion_total.outINDEL",breakpoint+".outINDEL.merge.outINS")
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
	contig_command=subprocess.Popen(['minimap2','-a',genome_mmi,'contig_all.fa'], stdout=subprocess.PIPE,stderr=devnull)
	contig_command_out_file=open("contig_all.minimap.splice.sam",'w')
	contig_command_out_file.write(contig_command.stdout.read().decode('utf-8'))	
	contig_command_out_file.close()
	from breakpoint_candidate_scripts.event_sv import event_sv
	event_sv("contig_all.minimap.splice.sam")
	from breakpoint_candidate_scripts.event_sv_INS import event_sv_INS
	event_sv_INS("contig_all.minimap.splice.sam.sv")
	from breakpoint_candidate_scripts.high_coverage import high_coverage
	high_coverage(chromosome,coverage)
	from breakpoint_candidate_scripts.Masked_genome import Masked_genome
	Masked_genome(genome_fa,chromosome)
	from breakpoint_candidate_scripts.bed import bed
	bed(chromosome)
	breakpoint_outINDEL("Candidate_SV.bed","blacklist.bed","Candidate_SV.outBlacklist.bed")
	breakpoint_outINDEL("Candidate_INDEL.bed","blacklist.bed","Candidate_INDEL.outBlacklist.bed")
	from breakpoint_candidate_scripts.vcf import vcf
	vcf(chromosome)
	from breakpoint_candidate_scripts.genotype import genotype
	genotype("Candidate_SV.vcf",bam,min_insert_size,max_insert_size)
	shutil.rmtree("assembly")
	os.chdir(root_path)

if __name__ == "__main__":
	chromosome,bam,genome_fa=sys.argv[1:]
	breakpoint_candidate(chromosome,bam,genome_fa)

