#!/usr/bin/env python
import subprocess,sys,re,getopt,os,warnings
import multiprocessing as mp

def usage():
	sys.exit('\nUsage:\n\nsource activate python3\nexport PATH=$PATH:ClipSV_install_directory/\n\nclipsv.py -b <bam/cram file> -g <genome.fa> [-dtphv]\n\n-b Indexed bam/cram file\n-g Fasta file of genome sequence (Should be indexed by Minimap2 "minimap2 -d genome.mmi genome.fa")\n\n----Optional---\n-t Threads (default: 3)\n-d Sequencing depth (default: automattically determined)\n-p Prefix (default: ClipSV_out)\n-v Version\n-h Help\n\n')

if sys.version_info[0] < 3:
	print('\nPlease Use Python3 !!\n')
	usage()

try:
	opts, args = getopt.getopt(sys.argv[1:], "b:g:d:t:p:h:v",["help"])
except getopt.GetoptError as err:
	print(err)
	usage()

bam,genome_fa,prefix='','','ClipSV_out'
if not opts:
	usage()
for o, a in opts:
	if o =="-b":
		bam=os.path.abspath(a)
	elif o =="-g":
		genome_fa=os.path.abspath(a)
	elif o =="-d":
		depth=int(a)
	elif o =="-t":
		threads=a
	elif o =="-p":
		prefix=a
	elif o =="-v":
		sys.exit('\nClipSV  v1.0\n\n')
	elif o in ("-h","--help"):
		usage()

if not bam:
	usage()
if not genome_fa:
	usage()

if os.path.exists(prefix):
	sys.exit('\nDirectory Already Exists!\n\n')
else:
	os.mkdir(prefix)
	os.chdir(prefix)

genome_m=re.search(r'^(.*)\.(fa|fasta)$',genome_fa)
if not genome_m:
	usage()
else:
	genome_mmi=genome_m.group(1)+'.mmi'

from clipsv_scripts.header import header
chromosomes=header(bam)

from clipsv_scripts.insert_size import insert_size
min_insert_size,max_insert_size,read_length,coverage=insert_size(bam,chromosomes[0])

try:
	coverage=depth
except NameError:
	pass

from clipsv_scripts.extract_breakpoints import extract_breakpoints
processes_1 = [mp.Process(target=extract_breakpoints, args=(x,bam,genome_mmi,min_insert_size,max_insert_size,read_length)) for x in chromosomes]
for p1 in processes_1:
	p1.start()
for p1 in processes_1:
	p1.join()

from clipsv_scripts.spliced_alignment import spliced_alignment
for x in chromosomes:
	spliced_alignment(x,bam,genome_mmi,coverage,threads)

from clipsv_scripts.breakpoint_candidate import breakpoint_candidate
processes_2 = [mp.Process(target=breakpoint_candidate, args=(x,bam,genome_fa,genome_mmi,coverage,min_insert_size,max_insert_size,read_length)) for x in chromosomes]
for p2 in processes_2:
        p2.start()
for p2 in processes_2:
        p2.join()

from clipsv_scripts.pool_vcf import pool_vcf
pool_vcf(chromosomes,prefix)

