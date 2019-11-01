# ClipSV (Structural variation detection with clipped reads)

A software to detect structural variations in human genomes by read extension, spliced alignment and local assembly.

Author: Peng Xu

Email: peng.xu@mssm.edu

Draft date: June. 4, 2019

## Description

ClipSV was developed to detect structural variations by read extension, spliced alignment and local assembly. It primarily depends on clipped reads from short-read sequencing platform. ClipSV was optimized to discover INDELS (5bp-50bp) and structural variations (>=50bp) in human genomes.

## System requirements and dependency

The program was tested on a x86_64 Linux system with 12 cores, each with a 4GB physical memory. The work can be usually finished within 6 hours per 30x whole genome sequencing sample.

Dependency: Python3, samtools (https://github.com/samtools/samtools), minimap2 (https://github.com/lh3/minimap2), bedtools (https://bedtools.readthedocs.io/en/latest/), velvet(https://www.ebi.ac.uk/~zerbino/velvet/) should be installed in current path.


## Installation

```
git clone https://github.com/penguab/ClipSV.git
```
Then, please also add this directory to your PATH:
```
export PATH=$PWD/ClipSV/:$PATH
```

## Usage

ClipSV needs two files as inputs. The first is an indexed bam/cram file from whole genome sequencing. The second is the genome reference indexed by minimap2 (To generate index file, use command "minimap2 -d genome.mmi genome.fa").
Quick start:
```
source activate python3
PATH=$PWD/ClipSV/:$PATH
clipsv.py  -t 12 -b bam/cram -g genome.fa
```

Parameters:
```
clipsv.py -b <bam/cram file> -g <genome.fa> [-dtphv]

-b Indexed bam/cram file
-g Fasta file of genome sequence (Should be indexed by Minimap2 "minimap2 -d genome.mmi genome.fa")

----Optional---
-t Threads (default: 3)
-d Sequencing depth (default: automatically determined)
-p Prefix (default: ClipSV_out)
-v Version
-h Help
```

## News

6/4/2019: First version released.

