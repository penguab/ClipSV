#!/usr/bin/env python
import subprocess,sys,re,getopt,os,warnings
import multiprocessing as mp

def usage():
	sys.exit('\nUsage:\nexport PATH=$PATH:ClipSV_install_directory/\nclipsv.py -b <bam file> -g <genome.mmi>\n')

if sys.version_info[0] < 3:
	print('\nPlease Use Python3 !!\n')
	usage()

try:
	opts, args = getopt.getopt(sys.argv[1:], "b:g:d:h",["help"])
except getopt.GetoptError as err:
	print(err)
	usage()

bam,genome='',''
if not opts:
	usage()
for o, a in opts:
	if o =="-b":
		bam=os.path.abspath(a)
	elif o =="-g":
		genome=os.path.abspath(a)
	elif o =="-d":
		depth=int(a)
	elif o in ("-h","--help"):
		usage()

if not bam:
	usage()
if not genome:
	usage()

from clipsv_scripts.header import header
chromosomes=header(bam)

from clipsv_scripts.insert_size import insert_size
min_insert_size,max_insert_size,read_length,fold=insert_size(bam,chromosomes[0])

try:
	fold=depth
except NameError:
	pass

from clipsv_scripts.extract_breakpoints import extract_breakpoints
processes_1 = [mp.Process(target=extract_breakpoints, args=(x,bam,genome,min_insert_size,max_insert_size,read_length)) for x in chromosomes]
for p1 in processes_1:
	p1.start()
for p1 in processes_1:
	p1.join()

from clipsv_scripts.spliced_alignment import spliced_alignment
for x in chromosomes:
	spliced_alignment(x,bam,genome,fold)

from clipsv_scripts.breakpoint_candidate import breakpoint_candidate
processes_2 = [mp.Process(target=breakpoint_candidate, args=(x,bam,genome,fold,min_insert_size,max_insert_size)) for x in chromosomes]
for p2 in processes_2:
        p2.start()
for p2 in processes_2:
        p2.join()

from clipsv_scripts.pool_vcf import pool_vcf
pool_vcf(chromosomes)

